# Soluciones de los ejercicios

> **No mires antes de intentar.** Cada respuesta indica el razonamiento, no solo el resultado. Los cálculos numéricos se verificaron con Python. Para diseño, hay **varias respuestas válidas**: se muestran los puntos que un evaluador esperaría.

---

# Fundamentos

**F-B1.** `I = 12/470 = 25.5 mA`. `P = V·I = 12·0.0255 = 0.306 W` (o `V²/R = 144/470 = 0.306 W`). 1/4 W (0.25 W) queda corto; con margen (≤ 50 %) se elige **1 W** (o mínimo 1/2 W, que ya se pasa del 50 %).

**F-B2.** `R = (3.3 − 2.0)/0.008 = 162.5 Ω`. Valor comercial cercano: **160 Ω** (E24) → `I = 1.3/160 = 8.1 mA`; con 180 Ω serían 7.2 mA.

**F-B3.** `V = 1000·3.3/4095 = 0.806 V` (con 4096: 0.806 V; diferencia despreciable). `LSB = 3.3/4096 = 0.806 mV`.

**F-B4.** **b).** La pull-up fija el nivel alto cuando nadie maneja la línea (evita entradas flotantes; es la base del *open-drain* en I2C/1-Wire).

**F-B5.** **b).** 3.3 V, no tolera 5 V; la corriente por pin es de pocos mA (verificar límites) y **no tiene ADC**.

**F-B6.** `(12−4)/16 = 50 %` → **5 bar**. Sobre 250 Ω: `V = 0.012·250 = 3.0 V` (rango 1–5 V).

**F-B7.** *Resolución*: mínimo cambio que se puede reportar (p. ej. 0.0625 °C del DS18B20 a 12 bits). *Exactitud*: cercanía al valor real (±0.5 °C). *Precisión/repetibilidad*: dispersión de medidas repetidas (σ). Se puede tener resolución 0.01 °C y exactitud ±1 °C.

**F-B8.** Para distinguir la señal mínima válida (4 mA) de una **falla de cable roto/sin alimentación (0 mA)**: *live zero*. Además permite alimentar el transmisor con el mismo lazo.

**F-I1.** `1/T = 1/298.15 + ln(20/10)/3950 = 0.0033540 + 0.0001755 = 0.0035295 → T = 283.33 K = 10.18 °C`. (R mayor → temperatura menor en una NTC.)

**F-I2.** Aliasing: `|1000 − 700| = 300 Hz` aparente. Se debió aplicar un **filtro anti-aliasing** (fc < 500 Hz) antes del ADC o muestrear a > 1.4 kHz (mejor 5–10×).

**F-I3.** `fc = 1/(2π·10 000·100·10⁻⁹) = 159 Hz`. Una señal de 1.6 kHz (~10× fc) se atenúa ≈ −20 dB (factor ~10) con un filtro de primer orden.

**F-I4.** `R_max = 300 ns / (0.8473 · 150 pF) = 2.36 kΩ`; `R_min = (3.3−0.4)/3 mA = 967 Ω`. Valor razonable: **1.5 kΩ–2.2 kΩ** (1.8 kΩ típico). A menor R, más corriente y más consumo, pero flancos más rápidos.

**F-I5.** `R_cable = 2·20 m·0.0175/0.5 = 1.4 Ω`; `ΔV = 0.15 A·1.4 Ω = 0.21 V` (1.75 % de 12 V). Aceptable; con sensores de baja tensión o mayor corriente habría que aumentar la sección.

**F-I6.** **b) 4** (`σ/√N = σ/√16`).

**F-I7.** Hay que **acondicionar la señal**: divisor. `R2/(10k+R2) ≤ 3.0/5 = 0.6 → R2 ≤ 15 kΩ`. Con **R2 = 15 kΩ** → 5 V → 3.0 V. (Tener en cuenta la impedancia de fuente del divisor: R1‖R2 = 6 kΩ; para ADC que pida < 10 kΩ está bien, si no, usar un buffer o condensador de muestreo; y la tolerancia de las resistencias.)

**F-I8.** No es correcto: `15·3.3/13.3 = 3.72 V > 3.3 V` (sobre el rango, riesgo de daño); a 12 V da 2.98 V. Fijar `R2/(R1+R2) ≤ 3.0/15 = 0.2` → `R2 ≤ 2.5 kΩ` → **R2 = 2.2 kΩ** (12 V → 2.16 V; 15 V → 2.70 V). Añadir zener/TVS y un RC contra transitorios.

**F-I9.** Lazo de tierra: dos puntos "GND" a potenciales distintos → circula corriente por el blindaje/masa y se acopla ruido. Mitigación: **masa en un solo punto** (estrella), blindaje a tierra en **un extremo**, **aislamiento galvánico**, señales diferenciales o 4–20 mA, cables lejos de potencia.

**F-I10.** **c) 85 °C** (valor de reset del scratchpad). −127 se ve cuando el bus lee 0xFF (sin dispositivo) en algunos drivers.

**F-A1.** Divisor `R1 = 4.7 kΩ` (arriba), `R2 = 10 kΩ`: `k = 10/14.7 = 0.680`. 4.5 V → 3.06 V; 0.5 V → 0.34 V. Cuentas 12 bits: `3.06/3.3·4095 ≈ 3799` y `0.34/3.3·4095 ≈ 422` → span ≈ **3377 cuentas** → `10 bar/3377 ≈ 2.96 mbar/LSB` (resolución del ADC; la exactitud real es la del sensor ±%FS). Limitaciones: (1) impedancia de salida del divisor 3.2 kΩ (verificar el ADC; añadir C de 100 nF y muestreo lento o buffer). (2) Sensor **ratiométrico**: la salida depende de la alimentación (5 V) → medir Vcc también, o usar el mismo Vref. (3) Tolerancia de las resistencias (1 %) afecta la ganancia. (4) Proteger contra sobretensión (zener/TVS). (5) Ruido: filtro RC + promedio.

**F-A2.** `P = (12 − 3.3)·0.2 = 1.74 W` (calor; el regulador se sobrecalienta sin disipador). Alternativa: **convertidor DC/DC reductor (buck)**, típicamente > 85 % de eficiencia (perdidas ≈ 0.1–0.2 W a esta carga), con filtro posterior si hay carga sensible.

**F-A3.** Problemas (≥ 5; hay más):
1. **7805 (5 V) con MCU/sensor de 3.3 V** → debería ser 3.3 V (o hay que adaptar niveles); un ESP32 no tolera 5 V.
2. **Pull-ups I2C a 5 V con dispositivos de 3.3 V** → sobretensión en pines; pull-ups a 3.3 V o level shifter.
3. Pull-ups de 10 kΩ pueden ser altas para 400 kHz/cable (calcular).
4. **1-Wire sin pull-up** (4.7 kΩ a 3.3 V) → nunca sube; y **modo parásito con 15 m** sin *strong pull-up* → poco fiable; usar VDD.
5. **Cable de 2 hilos sin trenzar** en paralelo con potencia del motor → EMI; usar par trenzado/blindado, separarlo.
6. **CAN sin transceptor** (el controlador da TX/RX lógicos, no CANH/CANL).
7. **120 Ω en cada uno de 3 nodos** → 40 Ω; deben ser **dos** (extremos).
8. **Sin fusible ni protección de polaridad/TVS** en alimentación de vehículo.
9. Regulador lineal 12 V→5 V con carga puede disipar mucho (mejor buck).
10. Falta desacople y protección de entradas.

**F-A4.** Respuesta modelo: 3 × **DS18B20** en vaina metálica, bus 1-Wire con **alimentación normal (VDD)**, par trenzado/CAT5 (DQ+GND en un par, VDD en otro), pull-up 4.7 kΩ (ajustar a la longitud; ~12 m con 3 sensores suele requerir revisar valor/topología lineal), resistencia serie ~100 Ω y TVS/diodos en el extremo del MCU, blindaje a tierra en un extremo. Alternativa robusta: **PT100/PT1000 con transmisor 4–20 mA** o convertidor digital RS-485 si el ruido es extremo. Muestreo 1 muestra cada 2–5 s (dinámica térmica lenta); validar por CRC, rango [−40,150], tasa de cambio y congelamiento; enviar `{sensor_id, value, unit, quality, seq}`. Diagnóstico: CRC inválido, −127, 85. Limitaciones: rango del DS18B20, tiempo de conversión 750 ms, medir carcasa ≠ bobinado.

**F-A5.** Nyquist = `fs/2 = 5 kHz`. Una componente de 7 kHz aparece como `|10 − 7| = 3 kHz` (alias). Evitarlo: filtro anti-aliasing analógico antes del ADC (fc ≈ 4 kHz), o sensor con filtro interno/mayor fs (sobremuestreo + decimación digital).

**F-A6.** `0x0191 = 401 → 25.0625 °C`; `0xFF5E = −162 → −10.125 °C`; `0x07D0 = 2000 → 125.0 °C` (máximo del rango); `0xFC90 = −880 → −55.0 °C` (mínimo).

**F-A7.** No necesariamente. **Resolución ≠ exactitud**: 16 bits dan 65 536 pasos, pero la exactitud depende de ruido, offset, ganancia, linealidad (INL/DNL), referencia y del propio sensor. Un ADC de 12 bits con buena referencia y bajo ruido puede ser más exacto que uno de 16 bits ruidoso. Se compara con **ENOB**, error total y estabilidad de Vref. Además, el sensor limita la exactitud del sistema.

---

# Protocolos

**P-B1.** **b) UART.**

**P-B2.** UART: 2 (TX, RX). I2C: 2 (SDA, SCL). 1-Wire: 1 (DQ). CAN: 2 (CANH, CANL). (GND aparte; UART con control de flujo añade RTS/CTS.)

**P-B3.** 8N1 = 10 bits por byte → `115200/10 = 11 520 B/s`. 100 B → `1000 bits/115 200 = 8.68 ms` (mínimo, sin pausas).

**P-B4.** **c)** En los dos extremos físicos del bus (dos en total).

**P-B5.** ≈ **60 Ω** (dos 120 Ω en paralelo). **120 Ω** → falta un terminador (o hay un cable abierto). **40 Ω** → tres terminadores (sobra uno).

**P-B6.** **b)** Sensor desconectado / bus a nivel alto constante (lectura 0xFF del driver) — validar CRC.

**P-B7.** ACK = confirmación tras cada byte: el receptor **tira SDA a 0** en el 9.º pulso de SCL. NACK (SDA en 1) = no confirmado (dirección inexistente, esclavo ocupado o fin de lectura del maestro).

**P-B8.** Protocolo = reglas de la trama (CAN: trama, ID, CRC; UART: start/datos/stop). Interfaz física = niveles y cableado (CAN ISO 11898-2: CANH/CANL diferencial; UART TTL/RS-232/RS-485). Transceptor = chip que adapta (TJA1051 para CAN; MAX3232 para RS-232). Ejemplo: un MCU con controlador CAN + TJA1051 + par trenzado; un MCU con UART + MAX485 → RS-485.

**P-I1.** `R_max = 1000 ns/(0.8473·300 pF) = 3.93 kΩ`; `R_min = 967 Ω`. Propuesta: **2.2 kΩ** (margen a ambos lados; verifica t_r real con osciloscopio).

**P-I2.** Sin conflicto: 0x68/0x69 + 0x48 son distintas (ponerlos con AD0 diferente). Con 3 MPU-6050 (solo 2 direcciones) → **multiplexor I2C (TCA9548A)**, otro bus I2C, o cambiar de sensor con más direcciones/SPI.

**P-I3.** 0x48 (p. ej. ADS1115), 0x68 (IMU/RTC), 0x76 (p. ej. BME280/BMP280) → **3 dispositivos** aparentes, en la imagen se ven 48, 68 y 76 (3). Si falta 0x76: alimentación, SDA/SCL, pull-ups, pin de dirección (0x77), dirección de 7 vs 8 bits, dispositivo en reset o en modo distinto (p. ej. CS a GND selecciona SPI en algunos módulos), soldadura.

**P-I4.** `0x0CF00400`: prioridad = `(0x0CF00400 >> 26) & 7 = 3`; PF = 0xF0 (≥ 240 → PDU2), PS = 0x04 → **PGN = 0xF004 = 61444** (EEC1); SA = 0x00. RPM: bytes 4–5 (índices 3–4) = `D0 39` → little-endian `0x39D0 = 14 800` → `14 800·0.125 = 1850 rpm`.

**P-I5.** `0x0191 = 401 → 25.0625 °C`. `0xFF5E = −162 → −10.125 °C`.

**P-I6.** El bit más significativo de cada ID va primero. `0x123 = 001 0010 0011`, `0x120 = 001 0010 0000` (11 bits). Coinciden en los primeros 9 bits; el primer bit distinto es el bit 1 (valor 2): `0x123` envía **recesivo (1)** mientras `0x120` envía **dominante (0)**; el bus queda en 0, el nodo `0x123` lo detecta, **pierde el arbitraje** y se retira; **gana 0x120** (ID menor = mayor prioridad) sin perder la trama. El perdedor reintenta al terminar.

**P-I7.** Orden: (1) baud rate y formato (8N1 vs 7E1) en ambos lados; (2) TX↔RX cruzados y **GND común**; (3) niveles (TTL 3.3/5 V vs RS-232) — medir con multímetro/osciloscopio; (4) loopback para aislar el lado; (5) osciloscopio: medir el ancho de bit = 1/baud; patrón 0x55; (6) precisión del reloj del MCU (cristal vs RC; error de divisor de baudios); (7) ruido/longitud de cable; (8) overrun/buffers.

**P-I8.** `150 · 128 = 19 200 bit/s`; `19 200/250 000 = 7.7 %` (con bit stuffing ~ 9 %). Carga baja y saludable.

**P-I9.** El bus es *open-drain*; sin pull-up la línea no sube a 1. Típico: **4.7 kΩ** a VDD (ajustar según longitud/capacitancia). Modo parásito: el sensor toma energía del propio DQ con VDD a GND (necesita *strong pull-up* durante la conversión); evitar en cables largos, muchos sensores o entornos ruidosos.

**P-I10.** CAN FD: hasta 64 B por trama (vs 8), fase de datos a mayor velocidad (BRS), CRC más largo. Un nodo **clásico** no entiende tramas FD y las trata como errores → no puede convivir si otros envían FD (todos deben soportar FD, o la red debe usar solo tramas clásicas).

**P-A1.** Comparación (ejemplo de respuesta): **1-Wire** simple y barato (8 DS18B20 en el mismo cable), pero 30 m con 8 sensores exige cuidado (topología lineal, pull-up/strong pull-up, cable trenzado; puede requerir maestros con *active pull-up* DS2482 o segmentar), velocidad baja, ruido industrial delicado. **RS-485/Modbus RTU** robusto hasta ~1 km, direccionamiento por esclavo, requiere un transmisor/convertidor por sensor (sensor Modbus) — más caro pero muy estándar en industria. **CAN** robusto, multi-maestro, mensajes por ID; requiere nodos con controlador+transceptor. Elección típica: **RS-485/Modbus** o **CAN** si el ambiente es ruidoso y crítico; 1-Wire si el presupuesto es bajo y el entorno moderado, dividiendo en 2 ramales de 15 m. Justificar con topología, ruido, mantenimiento y costo.

**P-A2.** Pruebas: (1) **bitrate** idéntico en todos; (2) resistencia CANH–CANL apagado ≈ 60 Ω; (3) voltajes en reposo ~2.5 V; (4) CANH/CANL no invertidos; (5) transceptor alimentado y TX/RX bien conectados; (6) presencia de al menos un nodo que dé ACK; (7) `candump -e` y osciloscopio (forma de onda diferencial). `ERROR-PASSIVE` con TX errores subiendo suele indicar **falta de ACK** (nadie más en el bus / bitrate distinto / terminación). Causas probables: bitrate, terminación, cableado.

**P-A3.** A mayor velocidad, el tiempo de subida requerido es menor (300 ns vs 1000 ns): la constante `R_pullup·C_bus` (t_r ≈ 0.8473·R·C) hace que con cable largo (C mayor) el flanco no alcance V_IH a tiempo. Soluciones: **bajar R de pull-up** (respetando 3 mA), **acortar el cable**, reducir dispositivos/capacitancia, **reducir velocidad**, usar *buffer/repetidor* I2C activo o cambiar a un bus diferencial (CAN/RS-485) para distancias mayores; par trenzado con GND entre SDA y SCL.

**P-A4.** GPS TTL (3.3 V) → MCU UART → **transceptor RS-485** (SP3485/MAX3485 de 3.3 V) con pin DE/RE controlado por el MCU (GPIO o auto-dirección); par trenzado blindado, **terminación 120 Ω** en los extremos, resistencias de polarización (*bias*) si hace falta; GND de referencia o aislado; velocidad ≤ 115 200 para 200 m es viable, verifica. Bytes perdidos: FIFO/DMA/interrupción, buffer circular, **checksum NMEA** para descartar líneas corruptas y resincronización por `$`, y control de flujo a nivel de aplicación (ACK) si es necesario.

**P-A5.** **CAN**: capas 1–2 (ISO 11898). **CANopen** (CiA 301): capa de aplicación con diccionario de objetos, NMT, PDO/SDO, heartbeat — automatización/motion. **J1939** (SAE): aplicación para vehículos pesados; 29 bit = prioridad + PGN + SA; 250 kbit/s típico; motores, camiones. **ISOBUS (ISO 11783)**: agricultura; basado en J1939, con terminal virtual y control de implementos.

**P-A6.** Si el maestro se reinicia a mitad de una transferencia, un esclavo puede haberse quedado enviando un 0 en un bit de dato y esperando pulsos de SCL: mantiene **SDA en 0** y el bus no se libera. *Recovery*: configurar SCL como GPIO, enviar **hasta 9 pulsos** de SCL hasta que SDA suba, generar STOP, reiniciar el periférico I2C; si persiste, reiniciar (power-cycle) el esclavo.
```
repetir hasta 9 veces: si SDA == 1 -> salir; pulso SCL (bajo, alto)
generar STOP (SDA sube con SCL alto); reinicializar el periférico I2C
```

**P-A7.** (1) **Solo escucha** (*listen-only*): no transmitir ni dar ACK. (2) **Autorización** del propietario/fabricante; leer el manual. (3) Conectar en el conector de diagnóstico, con **par trenzado** y sin interrumpir terminaciones ni añadir derivaciones largas. (4) **Aislamiento galvánico** del transceptor y protecciones (TVS/fusible). (5) No alimentar el gateway desde una línea que afecte el sistema; fusible en la alimentación. (6) Bitrate correcto (verificar). (7) Registrar sin decodificar comandos peligrosos; no reproducir tramas. (8) Probar primero en banco/simulador (`vcan`). (9) Considerar garantía y regulación.

**P-A8.** UART: `1000 bits / 9600 = 104 ms`. CAN FD: 100 B → 2 tramas (64 + 36 B); bits de datos ≈ 800; a 2 Mbit/s = 0.4 ms más el tiempo de arbitraje/encabezados/CRC a velocidad nominal → del orden de **~1 ms** en total. Comparación engañosa: hay overhead de encabezado, CRC/bit stuffing, arbitraje a velocidad nominal, ACK, distancia, transceptor, carga del bus y compartición con otros nodos; además UART es punto a punto y CAN es bus compartido.

---

# Programación

## C / C++

**PG-B1.** `s = (uint8_t)(300) = 44`; `t = 300`. Imprime **`44 300`**.

**PG-B2.** `x/y = 3` (división entera) y `(float)7/2 = 3.500000` → **`3 3.500000`**.

**PG-B3.** (a) `reg |= (1u << 3);` (b) `reg &= ~(1u << 5);` (c) `reg ^= (1u << 0);` (d) `(reg >> 7) & 1u` (e) `!(reg & (1u << 2))`.

**PG-B4.** **b).**

**PG-B5.** `const int *p`: el **dato** apuntado es de solo lectura (el puntero puede cambiar). `int *const p`: el **puntero** es fijo (el dato se puede modificar). `const int *const p`: ambos fijos.

**PG-B6.** `NULL`/`nullptr`: no apunta a ningún objeto. Desreferenciarlo es comportamiento indefinido (fallo de segmentación o, en MCU, lectura de la dirección 0). Se valida (`if (p == NULL) return ERROR;`) especialmente en parámetros de entrada y valores devueltos por `malloc`.

**PG-I1.** Errores: `sum` sin inicializar; `i <= n` lee `data[n]`; `sum / n` es división entera (y `n == 0` produce división por cero). Corrección: ver [`06_buggy_code.c`](../examples/c/06_buggy_code.c):
```c
static int average(const int *data, size_t n, float *out) {
    if (!data || !out || n == 0) return 0;
    long sum = 0;
    for (size_t i = 0; i < n; i++) sum += data[i];
    *out = (float)sum / (float)n;
    return 1;
}
```
**PG-I2.** (1) `buf[8]` desborda con `"sensor-12345"`; (2) se devuelve un puntero a memoria local (*dangling*) → UB. Corrección: el llamador pasa el buffer y su tamaño y se usa `snprintf(buf, size, ...)`.

**PG-I3.** 
```c
ctrl = (uint8_t)((ctrl & ~PRESC_MASK) | (5u << 4));   // PRESC_MASK = 0x70
ctrl = (uint8_t)((ctrl & ~MODE_MASK)  | (2u << 1));   // MODE_MASK  = 0x0E
```
Con `0x81`: limpiar 0x70 y 0x0E no cambia (ya son 0) → `0x81 | 0x50 | 0x04 = 0xD5`.

**PG-I4.** `lo = 0x34`, `hi = 0x12` → **`34 12`**.

**PG-I5.** `uint8_t` llega a 255 y luego da la vuelta a 0 (wrap), así que `i < 256` **siempre** es verdadero → bucle infinito. Usar `uint16_t`/`int` o `i <= 255` con cuidado.

**PG-I6.**
```c
#include <stdbool.h>
#include <stdlib.h>
bool parse_temp(const char *s, float *out) {
    if (!s || !out || *s == '\0') return false;
    char *end;
    float v = strtof(s, &end);              // convierte y detecta hasta dónde llegó
    if (end == s || *end != '\0') return false;   // no hubo número o hay basura al final
    if (v != v || v < -40.0f || v > 150.0f) return false;   // NaN o fuera de rango
    *out = v;
    return true;
}
```
**PG-I7.** Ver [`02_circular_buffer.c`](../examples/c/02_circular_buffer.c). En ISR + lazo principal: condiciones de carrera si se actualizan `count/head/tail` en ambos lados; soluciones: un solo productor y un solo consumidor con índices atómicos y sin `count` compartido, o proteger con sección crítica breve; usar `volatile` en los índices (no garantiza atomicidad en MCU de 8 bits); tamaño potencia de 2 para máscara.

**PG-I8.** En Linux/PC, `malloc` es habitual (memoria virtual, recursos abundantes). En MCU: poca RAM, **fragmentación**, tiempos no deterministas y fallos de asignación en campo; se evita en el lazo periódico y en ISR; se prefiere memoria estática/pools.

**PG-I9.** Una referencia es un alias no nulo de un objeto. `const std::string&` evita copiar la cadena (asignación en heap) y no permite modificarla; pasar por valor copia.

**PG-I10.** En `main` (arreglo local): `10`. En una función con `uint8_t *arr`: `sizeof(arr) = sizeof(puntero)` (4 u 8 bytes según la plataforma); por eso se pasa el tamaño aparte.

**PG-A1.** Ver el diagrama y [`04_state_machine.c`](../examples/c/04_state_machine.c). Tabla: INIT→SELF_TEST (periféricos OK); SELF_TEST→SAMPLING (sensores presentes) o FAULT; SAMPLING→VALIDATE (tick); VALIDATE→TRANSMIT (válida) o DEGRADED (inválida, `quality=BAD`); DEGRADED→SAMPLING; TRANSMIT→SAMPLING (ok) o NO_LINK (2 fallos); NO_LINK→SAMPLING (enlace vuelve) o SAFE (timeout largo); FAULT→SELF_TEST (reintento < N) o SAFE. **Watchdog** en el lazo principal, al final de un ciclo completo y sano (no en una ISR).

**PG-A2.** Ver [`03_serial_parser.c`](../examples/c/03_serial_parser.c). Resincronización: cualquier `$` reinicia el estado; buffer con límite; descarte ante `\n` inesperado; verificación de checksum y de formato numérico.

**PG-A3.** Lectura no atómica de un `uint32_t` en MCU de 8/16 bits: la ISR puede modificarlo entre lecturas de bytes → valor roto (*tearing*). Y la operación "leer y poner a 0" no es atómica → se pierden pulsos. Soluciones: (1) deshabilitar interrupciones brevemente para copiar y resetear (`__disable_irq()/__enable_irq()` o `noInterrupts()`); (2) contador libre + diferencias (`delta = actual − anterior` con lectura atómica); (3) variables de 8/16 bits o *atomics* del MCU.

**PG-A4.**
```cpp
uint32_t last = 0; const uint32_t PERIOD = 1000;
void loop() {
  uint32_t now = millis();
  if (now - last >= PERIOD) { last += PERIOD; tarea(); }   // sin delay()
}
```
Con `uint32_t`, la resta hace aritmética modular: el resultado correcto aunque `now` dé la vuelta (~49.7 días).

**PG-A5.** Timeouts en toda E/S; reintentos limitados; reinicio del periférico/bus (recovery I2C); validación de rango/CRC; marcar `quality=bad`; estado DEGRADED que sigue funcionando; contador de fallos y salida a FAULT/SAFE; watchdog; registro de causa de reset; alerta al gateway; no bloquear en la espera.

**PG-A6.** Endianness = orden de bytes de un valor multibyte. Little-endian: byte menos significativo primero (J1939 usa little-endian para campos de 16 bits). Para RPM 1850 (0x073A): LE `3A 07`, BE `07 3A`. Se serializa explícitamente con desplazamientos, no con `memcpy` de una `struct`/`uint16_t`.

## Python

**PY-B1.** Imprime **`[1, 2] [1, 2]`**: el valor por defecto mutable se crea una sola vez y se comparte. Corrección: `acc=None` y crear la lista dentro.

**PY-B2.** `[70, 95.5]` (−127 fuera del rango, 101 > 100).

**PY-B3.** Lista `[80.1, 80.3]` (ordenada, mutable); tupla `("tractor01", "temp")` (inmutable, hashable, clave de dict); dict `{"temp": 80.1, "unit": "C"}`; set `{"tractor01", "bomba02"}` (únicos, sin orden).

**PY-B4.** `with` cierra el archivo aunque ocurra una excepción (gestor de contexto), evitando fugas de descriptores.

**PY-B5.** **b).**

**PY-I1.**
```python
import math
from statistics import mean, median
def stats(values):
    v = [x for x in values if isinstance(x, (int, float)) and not isinstance(x, bool) and not math.isnan(x)]
    if not v: return None
    return {"min": min(v), "max": max(v), "mean": mean(v), "median": median(v)}
```
**PY-I2.** Ver [`03_read_csv.py`](../examples/python/03_read_csv.py) (`csv.DictReader`, `try/except ValueError`, `defaultdict(list)`, `enumerate(start=2)`).

**PY-I3.** Ver [`04_parse_json.py`](../examples/python/04_parse_json.py).

**PY-I4.** No hay `timeout` (puede colgarse), no maneja excepciones de red, no verifica `status_code`/`raise_for_status()`, y `.json()` falla si el cuerpo no es JSON o no tiene la clave `ok`. Corrección: `try: r = requests.post(URL, json=data, timeout=5); r.raise_for_status(); body = r.json() except (requests.RequestException, ValueError): ...`.

**PY-I5.** Ver [`06_post_to_api.py`](../examples/python/06_post_to_api.py). En el servidor: **idempotencia** con clave `(device_id, seq)` (o `Idempotency-Key`) y restricción única en BD (`ON CONFLICT DO NOTHING`).

**PY-I6.** Vida (termina vs meses); errores (un dato malo no debe tumbar el servicio); recursos (fugas); reinicio (systemd); señales (SIGTERM/cierre limpio); logs con rotación; configuración externa; concurrencia; monitoreo/heartbeat.

**PY-I7.** Ver [`07_timeout_detector.py`](../examples/python/07_timeout_detector.py). `monotonic()` no salta si cambia el reloj del sistema (NTP/ajuste manual); el reloj inyectable permite probar sin esperar.

**PY-I8.** Niveles, timestamps, múltiples destinos (consola/archivo/syslog), rotación, filtrado por módulo, `exception()` con traceback, formato estructurado. Ver [`10_logging_errors.py`](../examples/python/10_logging_errors.py) (`RotatingFileHandler`).

**PY-A1.** Hilo lector (serial → validación → `queue.Queue`) y hilo enviador (lee de la cola SQLite `outbox`, HTTP con reintentos); el lector escribe **primero en SQLite** (durable) — la cola en memoria solo desacopla; señales SIGTERM/SIGINT ponen una bandera `running=False` y se cierran puerto y BD; **orden** por `id` autoincremental; **no duplicados** con `(device_id, seq)` + servidor idempotente; borrar solo tras confirmación; heartbeat con `buffer_pending`.

**PY-A2.** Un `while True` que reintenta abrir/leer el puerto sin espera (busy loop) cuando lanza `SerialException`. Corrección: capturar la excepción, cerrar, **esperar con backoff** (`time.sleep`) y reabrir; registrar el evento una sola vez.

**PY-A3.** Ver [`09_alerts_thresholds.py`](../examples/python/09_alerts_thresholds.py). Casos: (1) una muestra alta aislada no alerta; (2) tres seguidas alertan; (3) oscilar 94–96 alrededor de 95 no genera muchos eventos; (4) baja a `< umbral − histéresis` limpia; (5) datos inválidos no cuentan.

**PY-A4.** UTC evita ambigüedades y saltos de horario de verano, y permite comparar dispositivos de distintas zonas; se convierte a hora local solo al mostrar. Guatemala **actualmente no usa** horario de verano, pero el diseño no debe depender de ello (los servidores/usuarios pueden estar en otras zonas; las reglas cambian). Verifica con `zoneinfo`.

**PY-A5.** `rms = sqrt(sum(x²)/N)`, `crest = max|x| / rms`. Línea base **por régimen** (carga/velocidad), umbral relativo (p. ej. 1.5× línea base) con confirmación de varias ventanas, exclusión de arranque/parada, y correlación con RPM/corriente. Ver [`vibration_anomaly.py`](../examples/python/vibration_anomaly.py).

## Git

**GIT-1.** Git = sistema de control de versiones local/distribuido; GitHub = plataforma que aloja remotos y añade PRs, issues, CI. `fetch` descarga sin integrar; `pull` = `fetch` + `merge`/`rebase`. `merge` conserva la historia con un commit de unión; `rebase` reaplica commits sobre otra base (historial lineal; no para ramas compartidas).

**GIT-2.**
```
git switch -c feature/x
git add -p && git commit -m "Paso 1" ; git commit -am "Paso 2"    # (con cambios preparados)
git push -u origin feature/x        # abrir Pull Request en la plataforma
git switch main && git pull         # tras el merge del PR
git branch -d feature/x
```
**GIT-3.** `git status` (both modified) → abrir el archivo → decidir el contenido final y quitar `<<<<<<<`, `=======`, `>>>>>>>` → `git add config.py` → `git commit` (o `git rebase --continue`) → **probar**. `git merge --abort` para cancelar.

**GIT-4.** (1) **Revocar/rotar la credencial** de inmediato (ya está en el historial y posiblemente en clones); (2) removerla del código y usar variables de entorno/archivo ignorado; (3) opcionalmente reescribir historia con `git filter-repo`/BFG y forzar el push, avisando al equipo — pero **rotar es lo esencial**; (4) añadir `.gitignore` y un escáner de secretos (pre-commit).

**GIT-5.** `git restore --source=HEAD~3 ruta/archivo` (o `git show HEAD~3:ruta/archivo`) recupera la versión sin tocar el resto. Deshacer un commit publicado: `git revert <hash>` (crea un commit inverso, no reescribe historia).

**GIT-6.** `__pycache__/`, `*.pyc`, `.venv/`, `.env`, `*.log`, `*.db`, `build/`, `*.o`, `*.elf`, `*.hex`, `.vscode/`, datos locales (`data/*.csv`), credenciales/llaves (`*.pem`). Conservar plantillas `config.example.*`.

## Embebidos

**EMB-1.** Polling: leer un sensor lento cada 1 s. Interrupción: contar pulsos de RPM o recibir bytes UART. Híbrido: la ISR solo marca una bandera o llena un buffer; el lazo principal procesa.

**EMB-2.** Reinicia el MCU si el software no lo "alimenta" a tiempo. Se alimenta en el lazo principal tras verificar que las tareas críticas progresaron; en una ISR seguiría alimentándose aunque el lazo esté colgado.

**EMB-3.** (a) Nodo sensor: Arduino/ESP32 (bajo costo, determinista). (b) Gateway: Raspberry Pi (Linux, Python, red, almacenamiento). (c) Tiempos estrictos: MCU (STM32/ESP32/Pico) o RTOS; Raspberry Pi con Linux estándar no garantiza latencia.

**EMB-4.** Causas: caída de tensión/brown-out por picos del Wi-Fi (fuente débil, sin condensadores), regulador insuficiente, watchdog por bloqueo, stack overflow, HardFault. Pruebas: leer la **causa del reset**, medir Vcc con osciloscopio durante la conexión, usar fuente robusta + 100–470 µF, deshabilitar Wi-Fi para ver si cesa, revisar pila.

**EMB-5.** `V_prom = 0.35 · 3.3 = 1.155 V`. Filtro RC paso bajo con `fc` ≪ 1 kHz (p. ej. R = 10 kΩ, C = 1 µF → 16 Hz) y buffer. Con PWM muy lenta el rizado en la salida es alto y la carga "ve" los pulsos.

---

# Linux

**L-B1.** `pwd` muestra el directorio actual; `ls -lah` lista con detalle, ocultos y tamaños legibles; `cd ..` sube; `mkdir -p` crea directorios y padres; `cp -r` copia recursivo; `mv` mueve/renombra; `rm -r` borra recursivo (¡cuidado!).

**L-B2.** `-rwxr-xr--`: dueño `gateway` (rwx), grupo `dialout` (r-x), otros (r--). Octal **754**. Es un archivo regular (`-`).

**L-B3.** `640`: dueño lee/escribe, grupo lee, otros nada. `chmod +x` añade el permiso de ejecución.

**L-B4.** `>` sobrescribe, `>>` añade. `2>&1` redirige stderr al mismo destino que stdout.

**L-B5.** Nodos de puertos seriales: `ttyUSB*` suele ser un convertidor USB-serie (FTDI, CH340, CP210x); `ttyACM*` dispositivos CDC-ACM (Arduino Uno R3/Leonardo, Pico). Ambos requieren permisos (grupo `dialout`/`uucp` según distribución).

**L-B6.** **b) `ss -tulpn`.**

**L-I1.** Diagnóstico: el usuario no pertenece al grupo dueño del dispositivo. `ls -l /dev/ttyUSB0` (grupo `dialout` en Debian/Ubuntu/Pi OS; puede ser `uucp`/`tty` en otras) → `id`/`groups` → `sudo usermod -aG dialout $USER` → **cerrar sesión/volver a entrar** (o `newgrp dialout`). Si aún falla: `fuser -v /dev/ttyUSB0` (otro proceso), `ModemManager`/`brltty`. Para servicios: `SupplementaryGroups=dialout` en la unidad.

**L-I2.**
```
systemctl status gateway.service
journalctl -u gateway.service -n 50 --no-pager
journalctl -u gateway.service -f
sudo systemctl restart gateway.service
```
**L-I3.** `grep -rniI "ERROR" /var/log/ | head` y contar: `grep -rciI "ERROR" /var/log/syslog` (por archivo) o `grep -rhiI "ERROR" /var/log | wc -l` (total). (`-n` número de línea, `-i` ignorar caso, `-r` recursivo, `-I` ignora binarios.)

**L-I4.** `find /opt/gateway -name "*.csv" -size +100M -mtime -1` (`-mtime -1` = modificados en las últimas 24 h).

**L-I5.**
```
python3 -m venv .venv && source .venv/bin/activate
pip install pyserial requests
pip freeze > requirements.txt
python app.py
```
**L-I6.** SIGTERM (15) pide terminar de forma ordenada (el programa puede limpiar); SIGKILL (9) mata sin aviso (no se puede capturar); SIGINT (2) es Ctrl+C. Se prefiere SIGTERM para cerrar puertos/archivos/vaciar buffers.

**L-I7.** `*/5 * * * * /opt/gateway/02_gateway_health.sh >> /var/log/gateway_health.log 2>&1`. Trampas: entorno mínimo (PATH), rutas relativas, permisos de ejecución, salida perdida si no se redirige, zona horaria del servidor, superposición de ejecuciones (usar `flock`).

**L-I8.** `scp datos.csv usuario@host:/opt/gateway/data/`; `rsync -avz ./app/ usuario@host:/opt/gateway/app/`. Claves: `ssh-keygen -t ed25519`, `ssh-copy-id usuario@host`, permisos `~/.ssh` 700 y `authorized_keys` 600; luego deshabilitar contraseña en `sshd_config` (probando antes de cerrar la sesión).

**L-I9.** `203/EXEC`: systemd no pudo ejecutar el comando: ruta de `ExecStart` errónea, falta permiso de ejecución, intérprete inexistente (`#!/usr/bin/env python` sin ese binario) o formato incorrecto. Revisar `ls -l`, `which`, la línea `#!`, `daemon-reload`.

**L-A1.** Usuario distinto (root vs `gateway`), **variables de entorno** (PATH, HOME), directorio de trabajo, grupos suplementarios (dialout), entorno virtual/intérprete, restricciones de seguridad (`ProtectSystem`, `ProtectHome`), red aún no disponible (`After=network-online.target`), dispositivo aún no presente, TTY/stdin ausente, límites de recursos.

**L-A2.** Ver [`gateway.service`](../examples/linux/gateway.service): `User=gateway`, `SupplementaryGroups=dialout`, `EnvironmentFile=`, `ExecStart=` (python del venv), `Restart=on-failure`, `RestartSec=5`, `WantedBy=multi-user.target`.

**L-A3.** `df -h` (qué partición), `df -i` (inodes), `du -xh --max-depth=1 / | sort -h | tail`, `sudo journalctl --disk-usage` / `journalctl --vacuum-size=200M`, `ls -lS`. Políticas: `logrotate`, rotación en la app, límites del journal (`SystemMaxUse`), límite del buffer, alerta al 80 %, mover datos históricos.

**L-A4.** Ver [`02_gateway_health.sh`](../examples/linux/02_gateway_health.sh). `set -e` sale ante error; `-u` trata variables no definidas como error; `-o pipefail` hace que un pipeline falle si falla algún tramo.

**L-A5.** Usar los enlaces estables `/dev/serial/by-id/...` (o `by-path`), o reglas **udev** que creen un nombre fijo (por `idVendor/idProduct/serial`), p. ej. `SYMLINK+="ttyGPS"`.

**L-A6.** `sudo ip link set can0 type can bitrate 250000 listen-only on && sudo ip link set can0 up && candump can0`. *Listen-only* evita transmitir y dar ACK: no altera el bus del vehículo. Ver [`04_can_socketcan.sh`](../examples/linux/04_can_socketcan.sh).

**L-A7.** Clave privada/pública no coinciden o no copiada (`ssh-copy-id`), usuario incorrecto, permisos de `~/.ssh` (700) o `authorized_keys` (600) o del home, `sshd_config` (`PubkeyAuthentication`), el agente ofrece otra clave (`ssh -v -i ...`). Prueba: `ssh -vvv`, revisar `journalctl -u ssh` en el servidor.

**L-A8.** Instalar globalmente con `pip` puede sobrescribir paquetes gestionados por el sistema (`apt`) y romperlo; PEP 668 marca el entorno como "externally managed" y `pip` se niega. Usar `venv`, `pipx` o paquetes `apt`.

---

# OT/IT

**OT-B1.** OT: tecnología que controla/monitorea procesos físicos; IT: sistemas de información. Diferencias: prioridad (OT disponibilidad/seguridad física vs IT confidencialidad), ciclo de vida (15–30 años vs 3–5), actualizaciones (difíciles y programadas vs frecuentes).

**OT-B2.** Monitoreo = leer/observar; control = actuar sobre el proceso. El alcance es **monitoreo** porque tiene menor riesgo, menos requisitos de seguridad funcional y se puede hacer sin intervenir el control de la máquina. Control exige análisis de riesgos, safety y validación.

**OT-B3.** **b) MQTT.**

**OT-B4.** Dispositivo que traduce protocolos (CAN/UART/Modbus → MQTT/HTTP), valida, agrega timestamp, bufferiza y conecta redes de forma controlada; centraliza seguridad y evita exponer cada dispositivo de campo.

**OT-B5.** PLC: controlador industrial robusto de ejecución cíclica. SCADA: supervisión y adquisición de datos. HMI: interfaz local operador-máquina. MES: ejecución de manufactura. ERP: gestión empresarial (finanzas, inventario).

**OT-B6.** TCP: orientado a conexión, fiable, ordenado (HTTP, MQTT, SSH). UDP: sin conexión, sin garantía, baja latencia (DNS, streaming, syslog).

**OT-B7.** **b)** 1883 / 8883.

**OT-I1.** El gateway sigue midiendo y guardando en un **buffer persistente** con el timestamp original, con reintentos y backoff; alerta local. Al volver: reenvía en orden con límite de velocidad y el servidor **ignora duplicados** (idempotencia por `device_id + seq`). Ver Caso D.

**OT-I2.** QoS 0: a lo más una entrega; QoS 1: al menos una (con ACK; puede haber duplicados si se pierde el ACK y se reenvía); QoS 2: exactamente una (handshake de 4 pasos, más costoso). Aún con QoS 2 se diseña idempotente por reinicios y reenvíos de la aplicación.

**OT-I3.** Campos: `device_id` (fuente), `ts` UTC (momento de medición), `seq` (orden/duplicados), `sensor`, `value`, `unit`, `quality`, y opcionalmente `schema` y `fw`. Ver módulo 11.

**OT-I4.** `ingenio/<sitio>/<maquina>/{telemetry,status,health}`; ACL: cada dispositivo solo **publica** en `ingenio/<sitio>/<su_id>/#` y no suscribe a otros; el servicio de ingesta suscribe `ingenio/+/+/telemetry`; el dashboard no se conecta al broker con permisos de escritura; usuarios únicos y TLS.

**OT-I5.** ISA-95: modelo funcional/de información para integrar sistemas empresariales y de control. Purdue: modelo de referencia por niveles para ubicar sistemas y segmentar redes. IEC 62443: normas de ciberseguridad (zonas, conductos, niveles de seguridad). Complementarios, no equivalentes.

**OT-I6.** Servicios expuestos sin autenticación; credenciales por defecto; protocolos sin cifrado (Modbus/TCP); ransomware/movimiento lateral; DoS a equipos frágiles; manipulación de comandos; falta de parches. Mitigación: sin puertos entrantes, DMZ, VPN/TLS, ACL, mínimo privilegio, segmentación, monitoreo y parches controlados.

**OT-I7.** `350·86 400 = 30.24 MB/día` por máquina; flota: `20 × 30.24 = 604.8 MB/día`. Con agregación cada 5 s: `6.05 MB/día` por máquina, `121 MB/día` la flota (reducción de 5×).

**OT-I8.** *Heartbeat*: mensaje periódico que indica que el dispositivo está vivo. *LWT*: mensaje que el broker publica si el cliente se desconecta sin aviso. *Keep-alive*: intervalo en el que el cliente debe comunicarse para mantener la conexión; también evita cierres por NAT ociosa.

**OT-I9.** Orden: (1) ¿el dato está en la BD (consulta directa)? (2) ¿llega al broker/API (`mosquitto_sub`, logs)? (3) ¿la ingesta lo inserta (logs, esquema)? (4) ¿la consulta del panel devuelve filas? (5) zona horaria/rango de tiempo; (6) filtros por `quality`/dispositivo/sensor; (7) caché/permisos de la fuente.

**OT-I10.** MQTT: telemetría continua, muchos dispositivos, redes inestables, empuje a múltiples suscriptores. HTTP/REST: lotes, consultas, integración simple, depuración con `curl`; ambos pueden combinarse.

**OT-A1.** Ver [`docs/15`](../docs/15_caso_realista_arquitectura.md) y [`architecture_case.html`](../diagrams/archify/architecture_case.html). Puntos esperados: capas (sensores→MCU→gateway→DMZ→servidor→dashboard), protocolos por enlace (1-Wire/I2C/CAN/UART/MQTT+TLS), zonas OT/IT, firewall solo saliente, buffer y reintentos, idempotencia, alertas (umbral + timeout), seguridad, y qué **no** se hace (control remoto, exposición a Internet).

**OT-A2.** Outbox SQLite (`id`, `payload`, `attempts`), enviador en lotes con backoff+jitter, `ack` → borrar solo tras confirmación, orden por `id`, límites del buffer (política de descarte + contador de descartes), servidor idempotente:
```sql
PRIMARY KEY (device_id, boot_id, seq);  -- y INSERT ... ON CONFLICT DO NOTHING
```
**OT-A3.** Riesgos: seguridad física/funcional (cavitación, sobrepresión, arranque inesperado), ciberseguridad (comando malicioso), disponibilidad y latencia, responsabilidad. Prerrequisitos: análisis de riesgos, límites y enclavamientos **en el control local** (PLC/variador con protecciones), autenticación fuerte (2FA), autorización por rol, registro/auditoría, comandos con confirmación y *timeout*, modo seguro por defecto. Fases: monitoreo → simulación/banco → comandos limitados en horario controlado → validación formal.

**OT-A4.** `5·300·86 400 = 129.6 MB`. Vaciar 86 400 mensajes a 50 msg/s: `86 400/50 = 1 728 s ≈ 28.8 min` (si siguen llegando 1 msg/s nuevos, neto 49 msg/s → ≈ 29.4 min).

**OT-A5.** Duplicados: reintentos/QoS 1/reenvío del buffer sin idempotencia. Timestamps en 1970: gateway sin hora tras reinicio (sin RTC/NTP) y se usó su reloj para `ts`. Correcciones: clave única `(device_id, boot_id, seq)` con `ON CONFLICT DO NOTHING`; RTC con batería + NTP; `ts_quality`; guardar `received_at`; esperar sincronización antes de marcar `ts` como confiable.

**OT-A6.** Autenticación: credenciales únicas o certificados por dispositivo; cifrado: TLS; actualizaciones: proceso controlado y firmado (diseño propio), inventario de versiones; acceso remoto: VPN + SSH por clave/2FA; sin puertos entrantes; secretos fuera del código; cifrar el disco si aplica; **si roban el equipo**: revocar sus credenciales/certificados, rotar secretos compartidos y revisar accesos.

**OT-A7.** Diodo de datos: hardware unidireccional (máxima garantía). DMZ: zona intermedia entre OT e IT. VPN: túnel cifrado y autenticado para acceso remoto/enlace entre sitios. Se usan combinadas según el nivel de riesgo.

**OT-A8.** 50 máquinas × 350 B/s = 17.5 kB/s = 140 kbit/s > 64 kbit/s → **excede** el enlace. Estrategia: agregación (1 msg/10 s con min/prom/máx → ~1.75 kB/s = 14 kbit/s), por excepción, compresión, batch, prioridad de alarmas (siempre inmediatas), *heartbeat* cada 60 s, buffer y envío diferido de series completas.
