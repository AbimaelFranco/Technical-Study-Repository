# Examen simulado · Ingeniero en Electrónica (60 minutos)

> **Instrucciones.**
> - Cronometra 60 minutos. Sin internet ni apuntes (o, para entrenar "prueba abierta", solo el [`QUICK_REFERENCE.md`](../QUICK_REFERENCE.md)).
> - Responde por escrito en un documento aparte, como si fuera una entrevista técnica virtual con pantalla compartida.
> - **Las soluciones están en [`solutions.md`](solutions.md): no las abras hasta terminar.**
> - Puntaje total: **100**. Aprobación de referencia: ≥ 70. Criterio: respuestas **correctas, justificadas y concisas**. Si no sabes algo, di qué **verificarías** y por qué.

| Sección | Tiempo | Puntos |
|---|---|---|
| 1. Fundamentos y protocolos | 15 min | 25 |
| 2. Programación (C/C++ y Python) | 20 min | 30 |
| 3. Linux y redes | 10 min | 15 |
| 4. Diseño de una solución industrial | 15 min | 30 |

---

## Sección 1 — Fundamentos y protocolos (15 min · 25 puntos)

**1.1 (2 pts, opción múltiple).** ¿Por qué un bus I2C necesita resistencias de pull-up?
a) Para limitar la corriente del maestro b) Porque las líneas son open-drain y los dispositivos solo pueden llevarlas a 0 c) Para filtrar ruido d) Para aumentar la velocidad del reloj

**1.2 (3 pts).** Un ADC de 12 bits con Vref = 3.3 V entrega la lectura 2500. (a) ¿Qué voltaje hay en la entrada? (b) Si el sensor es un LM35 (10 mV/°C), ¿qué temperatura resulta? (c) ¿Qué concluyes y qué revisarías?

**1.3 (3 pts).** Bus I2C a 3.3 V, 100 kHz (t_r,máx = 1000 ns), capacitancia total 200 pF. Calcula el rango de la pull-up (I_OL = 3 mA, V_OL = 0.4 V) y propón un valor.

**1.4 (2 pts).** Con un multímetro mides 60 Ω entre CANH y CANL con el bus apagado. ¿Qué indica? ¿Y si midieras 120 Ω?

**1.5 (3 pts).** UART a 9600 baud, 8N1. ¿Cuánto tarda en transmitirse un mensaje de 50 bytes (mínimo teórico)? ¿Y a 115 200 baud?

**1.6 (4 pts).** DS18B20: (a) convierte el valor crudo `0xFF5E` (16 bits, complemento a 2, 1/16 °C); (b) ¿qué significa una lectura de exactamente 85.0 °C?; (c) ¿y −127 °C leído en Linux?; (d) ¿qué compruebas para aceptar un dato?

**1.7 (4 pts).** Completa la tabla:

| | Nº de líneas de señal | Direccionamiento | Topología | Síncrono/asíncrono |
|---|---|---|---|---|
| UART | | | | |
| I2C | | | | |
| 1-Wire | | | | |
| CAN | | | | |

**1.8 (4 pts).** `i2cdetect -y 1` no muestra tu sensor. Da **cuatro pruebas ordenadas** (de la más simple a la más específica) y qué esperas ver en cada una.

---

## Sección 2 — Programación (20 min · 30 puntos)

**2.1 (5 pts, lectura de código C).** ¿Qué imprime y por qué?
```c
#include <stdio.h>
#include <stdint.h>
int main(void) {
    uint8_t reg = 0x81;
    reg = (uint8_t)((reg & ~0x70u) | (5u << 4));
    reg |= (1u << 2);
    reg &= ~(1u << 7);
    printf("0x%02X %d\n", reg, (reg >> 4) & 0x7);
    return 0;
}
```

**2.2 (8 pts, depuración C).** Encuentra **al menos 4 errores** y corrige la función:
```c
float avg_valid(int *data, int n) {
    int sum;
    int count;
    for (int i = 0; i <= n; i++) {
        if (data[i] > -40 && data[i] < 150) {
            sum += data[i];
            count++;
        }
    }
    return sum / count;
}
```

**2.3 (9 pts, diseño C).** Escribe una función en C que reciba un arreglo de `float`, su tamaño, y devuelva por un `struct` el **promedio, mínimo y máximo** de las lecturas **válidas** (válido = no NaN, distinto de −127 y dentro de [−40, 150]) y el número de válidas. Si no hay válidas, debe indicarlo sin dividir entre cero. Explica en 2 líneas su complejidad.

**2.4 (8 pts, Python).** Escribe `parse_reading(line: str)` que reciba una línea JSON de un dispositivo, p. ej. `{"id":"esp-01","seq":12,"temp_c":80.25,"quality":"good"}`, valide campos y tipos (`temp_c` puede ser `null` si `quality` es `"bad"`), y devuelva un diccionario o lance una excepción propia. Luego explica en 3 frases cómo usarías esta función en un servicio que lee del puerto serial **sin caerse** ante datos malos.

---

## Sección 3 — Linux y redes (10 min · 15 puntos)

**3.1 (3 pts).** Tu script Python falla con `PermissionError: [Errno 13] Permission denied: '/dev/ttyUSB0'`. Diagnostica y corrige (con comandos), y menciona la diferencia según distribución.

**3.2 (3 pts).** Escribe los comandos para: ver el estado del servicio `gateway.service`, ver las últimas 50 líneas de su log, y reiniciarlo.

**3.3 (3 pts).** Compara MQTT y HTTP/REST para enviar telemetría desde 20 máquinas por celular. ¿Cuál elegirías y por qué?

**3.4 (3 pts).** Explica la diferencia entre OT e IT y por qué se usa una DMZ y conexiones **salientes** desde el gateway.

**3.5 (3 pts).** ¿Qué debe ocurrir cuando se pierde Internet durante 3 horas y luego vuelve? Menciona cuatro elementos.

---

## Sección 4 — Diseño de una solución industrial (15 min · 30 puntos)

**Enunciado.** El ingenio tiene **5 bombas de riego con motor eléctrico** en campo, a 8 km de la oficina, con **cobertura celular intermitente** y alimentación de 220 V AC (en el tablero de cada bomba). Se pide monitorear **temperatura del motor**, **vibración del rodamiento** y **corriente**, generar **alertas** y tener **histórico**. **No** se debe controlar la bomba. Diseña la solución.

Entrega (usa viñetas y un diagrama de bloques en texto/ASCII):

| Parte | Puntos |
|---|---|
| **4.1** Diagrama de bloques (sensores → dashboard) | 5 |
| **4.2** Selección de componentes y protocolos con justificación | 5 |
| **4.3** Formato de datos (ejemplo JSON) y frecuencia de envío | 5 |
| **4.4** Estrategia sin conexión (buffer, reintentos, duplicados, hora) | 5 |
| **4.5** Validación de datos, diagnóstico y pruebas | 5 |
| **4.6** Seguridad y separación OT/IT; límites/supuestos de tu diseño | 5 |

---

## Al terminar
1. Suma tu puntaje con [`solutions.md`](solutions.md).
2. Anota **qué temas fallaron** y repásalos con [`STUDY_PLAN.md`](../STUDY_PLAN.md) / [`INDEX.md`](../INDEX.md).
3. Repite en 3 días **solo** las preguntas fallidas.
