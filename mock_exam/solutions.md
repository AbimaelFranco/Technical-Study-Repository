# Soluciones y criterios · Examen simulado (60 min)

> Abre este archivo **después** de resolver [`exam_60min.md`](exam_60min.md). Para cada pregunta: **respuesta**, **explicación**, **criterio de puntaje** y **errores frecuentes**. Los cálculos se verificaron con Python.

---

## Sección 1 — Fundamentos y protocolos (25 pts)

### 1.1 (2 pts) — **b)**
Las líneas SDA/SCL son *open-drain*: un dispositivo solo puede llevarlas a 0; la pull-up devuelve la línea a 1. *Puntaje:* 2 correcto; 0 otra. *Error frecuente:* elegir (a): no es para limitar corriente del maestro.

### 1.2 (3 pts)
(a) `V = 2500 · 3.3 / 4095 = 2.015 V` (1 pt). (b) `2.015 V / 10 mV/°C = 201.5 °C` (1 pt). (c) **No es plausible** (fuera del rango del LM35, ≈ −55…150 °C, y de la operación normal): revisar si es sensor desconectado/saturación de ADC, unidad/escala, alimentación de 5 V vs Vref de 3.3 V, ruido o cortocircuito; comprobar con multímetro y aplicar **validación de plausibilidad** (1 pt). *Error:* aceptar 201 °C como dato.

### 1.3 (3 pts)
`R_max = 1000 ns / (0.8473 · 200 pF) = 5.90 kΩ`; `R_min = (3.3 − 0.4) / 3 mA = 967 Ω` (2 pts). Valor sugerido: **2.2 kΩ–4.7 kΩ** (p. ej. 4.7 kΩ es habitual a 100 kHz; con margen 3.3 kΩ) (1 pt). *Error:* dar solo un valor sin justificación; usar 5 V en el cálculo mínimo.

### 1.4 (2 pts)
60 Ω = **dos terminadores de 120 Ω en paralelo** (bus terminado correctamente en sus extremos) (1 pt). 120 Ω = **falta un terminador** (o un tramo abierto) (1 pt).

### 1.5 (3 pts)
8N1 → 10 bits/byte. 50 B = 500 bits. A 9600: `500/9600 = 52.1 ms` (1.5 pt). A 115 200: `500/115 200 = 4.34 ms` (1.5 pt). *Error:* olvidar los bits de start/stop y calcular con 8 bits (41.7 ms).

### 1.6 (4 pts)
(a) `0xFF5E = 65374 − 65536 = −162 → −162/16 = −10.125 °C` (1 pt). (b) 85.0 °C es el **valor de reset**: probablemente se leyó sin conversión completada (1 pt). (c) −127 °C: bus en alto/sin dispositivo (lectura 0xFF), sensor desconectado (1 pt). (d) **CRC válido** del scratchpad, rango plausible, y que la conversión haya terminado (1 pt).

### 1.7 (4 pts)
| | Líneas | Direccionamiento | Topología | Sinc./asinc. |
|---|---|---|---|---|
| UART | 2 (TX, RX) | Ninguno | Punto a punto | Asíncrono |
| I2C | 2 (SDA, SCL) | 7/10 bits | Bus (multi-maestro posible) | Síncrono |
| 1-Wire | 1 (DQ) | ROM de 64 bits | Bus (un maestro) | Asíncrono (slots) |
| CAN | 2 (CANH, CANL) | ID 11/29 bits (por contenido) | Bus lineal, terminadores en extremos | Asíncrono |

*Puntaje:* 1 pt por fila correcta. *Aceptable:* "3 con GND" si se aclara.

### 1.8 (4 pts) — respuesta modelo
1. **Alimentación y GND** del sensor con multímetro (VCC correcto, masa común).
2. **SDA y SCL en reposo ≈ Vcc** (presencia de pull-ups); si ≈ 0 V hay corto o esclavo bloqueando.
3. **I2C habilitado y bus correcto** (`ls /dev/i2c-*`, bus 1) y direcciones posibles (ADDR, 7 vs 8 bits).
4. **Analizador lógico/osciloscopio:** ¿START + dirección + ACK? Si NACK: dirección/velocidad/niveles; probar con solo ese dispositivo y bajar la velocidad.
*Puntaje:* 1 pt por prueba pertinente **y** en orden razonable con el resultado esperado. *Error:* saltar a "cambiar el sensor" sin medir.

---

## Sección 2 — Programación (30 pts)

### 2.1 (5 pts)
`0x81` → limpiar bits 6..4 → `0x81`; `| (5<<4)=0x50` → `0xD1`; `|= 0x04` → `0xD5`; `&= ~0x80` → `0x55`. Imprime **`0x55 5`** (`(0x55 >> 4) & 7 = 5`). *Puntaje:* 3 pts por `0x55`, 2 pts por `5`; razonamiento paso a paso obtiene el puntaje aunque falle un paso menor.

### 2.2 (8 pts) — errores (2 pts c/u, mínimo 4)
1. `sum` **sin inicializar** → `int sum = 0`.
2. `count` **sin inicializar** → `int count = 0`.
3. `i <= n` lee `data[n]` (fuera de límites) → `i < n`.
4. **División entera** `sum / count` → devolver `float`, `(float)sum / count`.
5. **División entre cero** si `count == 0` → validar.
6. Puntero `data` sin validar y límite de rango exclusivo (>-40 y <150 excluye los extremos, decidir) → validar `data != NULL`, `n > 0`.
Versión corregida:
```c
#include <stddef.h>
static int avg_valid(const int *data, size_t n, float *out) {
    if (!data || !out || n == 0) return 0;
    long sum = 0; size_t count = 0;
    for (size_t i = 0; i < n; i++)
        if (data[i] >= -40 && data[i] <= 150) { sum += data[i]; count++; }
    if (count == 0) return 0;
    *out = (float)sum / (float)count;
    return 1;
}
```

### 2.3 (9 pts)
```c
#include <math.h>
#include <stddef.h>
typedef struct { float mean, min, max; size_t valid; } Stats;
static int is_valid(float t) { return !isnan(t) && t != -127.0f && t >= -40.0f && t <= 150.0f; }
static Stats compute(const float *d, size_t n) {
    Stats s = {0, 0, 0, 0};
    double sum = 0;
    for (size_t i = 0; i < n; i++) {
        if (!is_valid(d[i])) continue;
        if (s.valid == 0 || d[i] < s.min) s.min = d[i];
        if (s.valid == 0 || d[i] > s.max) s.max = d[i];
        sum += d[i]; s.valid++;
    }
    if (s.valid) s.mean = (float)(sum / s.valid);
    return s;
}
```
Criterios: validación correcta de los tres casos (2 pts); inicialización de min/max con la primera válida (2 pts); acumulación sin desbordar (double/long) (1 pt); manejo de `valid == 0` (2 pts); estructura clara/const-correcta (1 pt); complejidad **O(n) tiempo, O(1) memoria** (1 pt). *Errores:* inicializar min = 0 o max = 0; incluir −127; no comprobar `NaN` con `==`.

### 2.4 (8 pts)
```python
import json

class InvalidReading(ValueError): pass

def parse_reading(line: str) -> dict:
    try:
        obj = json.loads(line)
    except json.JSONDecodeError as e:
        raise InvalidReading(f"JSON invalido: {e}") from e
    if not isinstance(obj, dict): raise InvalidReading("no es un objeto")
    if not isinstance(obj.get("id"), str): raise InvalidReading("id")
    seq = obj.get("seq")
    if not isinstance(seq, int) or isinstance(seq, bool): raise InvalidReading("seq")
    quality = obj.get("quality")
    if quality not in ("good", "uncertain", "bad"): raise InvalidReading("quality")
    t = obj.get("temp_c")
    if t is None:
        if quality != "bad": raise InvalidReading("temp_c null solo con quality=bad")
    elif not isinstance(t, (int, float)) or isinstance(t, bool) or t != t:
        raise InvalidReading("temp_c")
    return obj
```
Criterios: manejo de `JSONDecodeError` (2), validación de campos/tipos incl. `bool` (2), regla `null`⇔`bad` (2), excepción propia (1), explicación del servicio (1): lazo `while running:` con `readline()` con timeout, `try/except InvalidReading` que **registra y continúa**, contador de errores/`logging`, reconexión del puerto con backoff y SIGTERM para cerrar limpio.

---

## Sección 3 — Linux y redes (15 pts)

### 3.1 (3 pts)
El usuario no pertenece al grupo dueño del dispositivo. `ls -l /dev/ttyUSB0` → grupo (normalmente **`dialout`** en Debian/Ubuntu/Raspberry Pi OS; en otras distros puede ser `uucp` o `tty`). Solución: `sudo usermod -aG dialout $USER` y **cerrar sesión/volver a entrar** (1 pt diagnóstico, 1 pt comando, 1 pt nota sobre distro/re-login). Alternativas: para un servicio, `SupplementaryGroups=`; comprobar que otro proceso no use el puerto (`fuser`). *Error:* `chmod 777 /dev/ttyUSB0` o ejecutar todo con `sudo`.

### 3.2 (3 pts)
```
systemctl status gateway.service
journalctl -u gateway.service -n 50 --no-pager
sudo systemctl restart gateway.service
```
1 pt cada uno.

### 3.3 (3 pts)
Elección razonable: **MQTT** (publicar/suscribir, cabecera pequeña, conexión persistente, QoS 1, LWT, mejor con enlaces celulares inestables); mencionar TLS y que HTTP/REST es válido si se envía por lotes y se prioriza simplicidad. Puntaje: elección justificada (2), mención de QoS/duplicados o buffer (1). *Error:* "MQTT siempre es mejor".

### 3.4 (3 pts)
OT controla procesos físicos (prioridad disponibilidad/seguridad; ciclo de vida largo; parches difíciles); IT maneja datos (confidencialidad; ciclo corto) (1.5 pts). La **DMZ** evita comunicación directa IT↔OT; el gateway usa **conexiones salientes** para no abrir puertos entrantes en OT y reducir la superficie de ataque (1.5 pts).

### 3.5 (3 pts)
Al menos cuatro: **buffer local persistente**, **timestamp original**, **reintentos con backoff**, **idempotencia (`device_id + seq`)**, envío limitado/en orden al recuperar, heartbeat/alerta local, reloj (NTP/RTC). 0.75 pt cada uno hasta 3.

---

## Sección 4 — Diseño de una solución industrial (30 pts)

### Solución de referencia (una de varias válidas)

**4.1 Diagrama de bloques (5 pts)**
```
[DS18B20 x2] --1-Wire--\
[Acelerometro MEMS] --SPI/I2C--> [Nodo MCU (STM32/ESP32)] --UART/RS-485--> [Gateway Linux (RPi)]
[Sensor de corriente Hall/CT] --ADC--/                                  |  Buffer SQLite
                                                                        |  (modem LTE + VPN/TLS)
                                                                        v
                            ---------- Internet (celular) ----------> [Firewall/DMZ -> Broker MQTT TLS]
                                                                        v
                                                     [Ingesta -> PostgreSQL -> Dashboard + Alertas]
```
Criterios: flujo completo (2), zonas OT/IT y frontera (1), buffer/borde (1), alertas (1).

**4.2 Componentes y protocolos (5 pts)**
- Temp.: DS18B20 en vaina (1-Wire) — digital, ID único; o PT100 si se requiere mayor exactitud/rango.
- Vibración: MEMS (I2C/SPI) montaje rígido; procesar en MCU (RMS, pico, bandas) con fs ≥ 5–10× la banda de interés (con filtro anti-aliasing).
- Corriente: Hall/CT + ADC con aislamiento (o medidor Modbus RTU si ya existe).
- Nodo MCU: determinismo, watchdog; UART/RS-485 al gateway (RS-485 si hay distancia > pocos metros).
- Gateway: Raspberry Pi/industrial: Linux, Python, buffer SQLite, systemd, VPN.
- Enlace: LTE con antena externa; MQTT/TLS QoS 1.
- Servidor: broker + PostgreSQL/TimescaleDB + Grafana/Django.
- Alimentación desde 220 V AC: fuente AC/DC industrial con protecciones (fusible, varistor/TVS) y **respaldo/UPS** o supercondensador para apagado ordenado. *(La instalación eléctrica en 220 V requiere personal calificado.)*
Criterios: justificación por elemento (3), alimentación/protección (1), coherencia entre protocolos y distancias (1).

**4.3 Formato de datos y frecuencia (5 pts)**
```json
{"schema":1,"device_id":"bomba03","boot_id":4,"seq":1201,"ts":"2026-03-01T14:03:22Z","fw":"1.0.0",
 "readings":[{"sensor":"temp_motor","value":78.4,"unit":"C","quality":"good"},
             {"sensor":"vib_rms","value":2.1,"unit":"mm/s","quality":"good"},
             {"sensor":"corriente","value":18.7,"unit":"A","quality":"good"}]}
```
Frecuencia: temperatura/corriente cada 5–10 s (o promedio por 10 s); vibración: indicadores por ventana cada 10 s (no forma de onda cruda); heartbeat cada 30–60 s; alarmas inmediatas. Criterios: campos esenciales (`device_id`, `ts` UTC, `seq`, unidad, `quality`) (3), justificación de frecuencia (1), agregación/excepción para reducir datos (1).

**4.4 Sin conexión (5 pts)**
Outbox SQLite persistente; `ts` original del momento de medición; reintentos con backoff+jitter; envío en lotes ordenados con límite de tasa; **idempotencia** `(device_id, boot_id, seq)` con `ON CONFLICT DO NOTHING`; límite del buffer y contador de descartes; RTC/NTP; alerta local (LED) y heartbeat con `buffer_pending`; capacidad ejemplo: 10 s por mensaje × ~350 B ≈ 3 MB/día. Criterios: buffer persistente (1), timestamp (1), reintentos (1), duplicados (1), límites/reloj (1).

**4.5 Validación, diagnóstico y pruebas (5 pts)**
Validación en 3 niveles (MCU: CRC/rango/tasa de cambio; gateway: plausibilidad/congelamiento/correlación temp-corriente; servidor: esquema); `quality` en cada dato; diagnóstico con la **lista por capas** (alimentación → bus → protocolo → software → red → datos); pruebas: banco, integración, desconexión de red/energía, ambiental, piloto con referencia calibrada; criterios de aceptación medibles.

**4.6 Seguridad y OT/IT (5 pts)**
Sin puertos entrantes, conexiones **salientes** con TLS; credenciales únicas por dispositivo y ACL por topic; VPN + SSH por clave para mantenimiento; firewall deny-by-default; DMZ para el broker; sin control remoto (**solo monitoreo**); actualizaciones controladas; secretos fuera del código. **Supuestos/límites:** cobertura celular, umbrales definidos por el fabricante, calibración, la alarma no reemplaza protecciones de seguridad del motor, requisitos eléctricos/normativos por verificar. Criterios: seguridad concreta (3), separación OT/IT (1), supuestos/límites explícitos (1).

---

## Errores frecuentes del simulacro (checklist de corrección)
- Aceptar valores imposibles (201 °C, −127 °C, 85 °C) sin cuestionar.
- Olvidar start/stop bits en UART; confundir 60 Ω con 120 Ω en CAN.
- Pull-ups sin cálculo ni justificación.
- Código C sin inicializar variables ni validar entradas; división entera.
- Servicios Python que se caen por un dato malo o sin timeout.
- Diseño que **expone la red de control a Internet** o usa hora de llegada en vez de la de medición.
- Diseño de control cuando se pidió monitoreo.
- No declarar supuestos ni qué verificar en datasheets.

## Tabla de puntaje
| Sección | Máx. | Tu puntaje |
|---|---|---|
| 1 Fundamentos y protocolos | 25 | |
| 2 Programación | 30 | |
| 3 Linux y redes | 15 | |
| 4 Diseño industrial | 30 | |
| **Total** | **100** | |

**Interpretación (referencia):** ≥ 85 excelente · 70–84 listo con repaso puntual · 50–69 repasar módulos débiles (usa el plan de estudio) · < 50 reforzar fundamentos y repetir.
