# Ejercicios · Protocolos de comunicación (UART, I2C, 1-Wire, CAN)

> Soluciones en [`answer_key.md`](answer_key.md) (sección **Protocolos**). Teoría: [`docs/02_protocolos_comunicacion.md`](../docs/02_protocolos_comunicacion.md).

## Nivel básico

**P-B1 (MC).** ¿Cuál protocolo es asíncrono y punto a punto?
a) I2C b) UART c) CAN d) 1-Wire (multipunto)

**P-B2 (C).** Completa la tabla: ¿cuántos conductores de señal usa cada protocolo (sin contar alimentación/GND)? UART, I2C, 1-Wire, CAN.

**P-B3 (CAL).** UART a 115 200 baud, formato 8N1. ¿Cuántos bytes útiles por segundo como máximo? ¿Cuánto tarda en enviarse un mensaje de 100 bytes?

**P-B4 (MC).** ¿Dónde se colocan las resistencias de terminación de 120 Ω en un bus CAN?
a) En cada nodo b) Solo en el nodo maestro c) En los dos extremos del bus d) No se necesitan a baja velocidad

**P-B5 (C).** ¿Qué medirías con un multímetro entre CANH y CANL con el bus apagado y correctamente terminado? ¿Y si mides 120 Ω? ¿Y 40 Ω?

**P-B6 (MC).** Un DS18B20 lee `-127 °C` en Linux. Lo más probable es:
a) Temperatura real b) Sensor desconectado / bus a nivel alto c) Sobretemperatura d) Error de calibración

**P-B7 (C).** ¿Qué es un *ACK* en I2C y quién lo genera?

**P-B8 (C).** ¿Cuál es la diferencia entre protocolo, interfaz física y transceptor? Da un ejemplo con CAN y otro con UART.

## Nivel intermedio

**P-I1 (CAL).** Bus I2C a 3.3 V, 100 kHz, capacitancia de 300 pF. Calcula la pull-up máxima (t_r,máx = 1000 ns) y la mínima (I_OL = 3 mA, V_OL = 0.4 V). Propón un valor.

**P-I2 (CAL).** Dos MPU-6050 (dirección 0x68 o 0x69 según AD0) y un ADS1115 (0x48) en el mismo bus. ¿Hay conflicto? Si necesitas 3 MPU-6050, ¿qué haces?

**P-I3 (LEC).** `i2cdetect -y 1` muestra:
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
40: -- -- -- -- -- -- -- -- 48 -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- 76 --
```
¿Qué dispositivos hay (direcciones de 7 bits)? ¿Cuántos? ¿Qué harías si falta el de 0x76?

**P-I4 (CAL).** Un gateway J1939 lee la trama con ID `0x0CF00400`, datos `FF FF FF D0 39 FF FF FF`. Extrae prioridad, PGN, dirección de origen y las RPM (SPN 190: bytes 4–5, little-endian, 0.125 rpm/bit).

**P-I5 (CAL).** Convierte el scratchpad del DS18B20: bytes `0x91 0x01` (LSB, MSB). Y `0x5E 0xFF`.

**P-I6 (C).** Explica el arbitraje de CAN con dos nodos que transmiten simultáneamente los IDs `0x123` y `0x120`. ¿Quién gana y por qué?

**P-I7 (C).** UART: recibes caracteres corruptos. Lista 6 causas ordenadas por facilidad de verificación y cómo las comprobarías.

**P-I8 (CAL).** Un bus CAN a 250 kbit/s transporta 150 tramas/s extendidas de 8 bytes (≈ 128 bits sin stuffing). Calcula la carga aproximada del bus.

**P-I9 (C).** ¿Por qué 1-Wire necesita una pull-up y cuál es un valor típico? ¿Qué es el modo parásito y cuándo evitarlo?

**P-I10 (C).** Diferencia entre CAN clásico y CAN FD. ¿Puede un nodo CAN clásico convivir en un bus donde otros envían tramas FD?

## Nivel avanzado

**P-A1 (DIS).** Tienes 8 sensores de temperatura distribuidos a lo largo de 30 m en una tubería. Compara 1-Wire, RS-485 (Modbus RTU) y CAN. Elige uno y justifica (topología, distancia, robustez, direccionamiento, costo, código).

**P-A2 (DEP).** "CAN no comunica": tienes dos nodos a 250 kbit/s; en `candump` no aparece nada; `ip -details -statistics link show can0` muestra `ERROR-PASSIVE` y el contador TX de errores sube. Da una lista ordenada de pruebas y las causas más probables.

**P-A3 (DEP).** Un I2C funciona a 100 kHz pero falla a 400 kHz con cable de 60 cm. Explica físicamente por qué y da soluciones.

**P-A4 (DIS).** Necesitas leer un GPS (NMEA a 9600 baud) y enviar los datos por RS-485 a 200 m. Diseña la conexión (niveles, transceptores, control de dirección) y explica cómo manejarías la pérdida de bytes.

**P-A5 (C).** CAN vs CANopen vs J1939 vs ISOBUS: para cada uno, ¿qué capa define y en qué contexto se usa?

**P-A6 (DEP).** Un bus I2C queda "colgado" con SDA en 0 tras reiniciar el maestro. ¿Por qué ocurre y cómo se recupera? Escribe el pseudocódigo del *bus recovery*.

**P-A7 (DIS).** Estás escuchando el CAN de un tractor. Enumera al menos 6 precauciones (eléctricas, de software y de seguridad).

**P-A8 (CAL).** Se transmite un mensaje de 100 bytes por UART a 9600 baud 8N1 y por CAN FD (64 B por trama, fase de datos a 2 Mbit/s, ignora overhead). Compara tiempos aproximados y comenta por qué la comparación es engañosa.

## Práctica en banco (sin respuesta única)
1. Con un adaptador USB-serie y un cable, haz *loopback* (TX↔RX) y envía un texto con `screen`/`pyserial`.
2. Con `examples/python/i2c_multisensor.py --demo-missing 0x68` comprueba cómo un dispositivo ausente no detiene a los demás.
3. Con `examples/python/can_j1939_decode.py` añade el decodificador de otra PGN (busca los datos en el DBC/especificación **oficial** del equipo que uses).
4. Dibuja en papel el bus CAN de 3 nodos con terminadores y marca dónde medirías 60 Ω.
