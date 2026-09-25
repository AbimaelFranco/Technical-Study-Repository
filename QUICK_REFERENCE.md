# Hoja de repaso intensiva (Quick Reference)

> Imprímela o tenla abierta en la última hora antes de la prueba. Cada bloque enlaza a su módulo. **Los valores marcados con ≈ o "típico" dependen del dispositivo: verifica en el datasheet.**

## 1. Protocolos: tabla comparativa

| Protocolo | Sincronización | Serial/paralelo | Líneas | Reloj | Topología | Dispositivos | Direccionamiento | Velocidad típica | Distancia típica | Duplex | Ventajas | Limitaciones | Aplicación ideal |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **UART** | Asíncrona | Serial | TX, RX (+GND) | No | Punto a punto | 2 | Ninguno | 9600–115200 baud (más con HW) | Metros (TTL); RS-485 hasta cientos de m | Full | Simple, universal | Sin direcciones ni CRC nativo, baud acordado | GPS, módems, consola |
| **I2C** | Síncrona | Serial | SDA, SCL | Sí | Bus | Decenas (C_b ≤ 400 pF) | 7/10 bits | 100 k / 400 kHz (1 M, 3.4 M) | ≤ ~1 m | Half | 2 hilos, ACK, muchos sensores | Corto alcance, pull-ups, direcciones | Sensores en placa |
| **1-Wire** | Asíncrona (slots) | Serial | DQ (+GND) | No | Bus | Muchos | ROM 64 bits | ≈ 15 kbit/s | Decenas de m (buenas prácticas) | Half | 1 hilo, ID único | Lento, timing crítico | DS18B20 distribuidos |
| **CAN** | Asíncrona | Serial | CANH, CANL | No | Bus lineal + 2 × 120 Ω | Decenas | ID 11/29 bits | 125 k–1 Mbit/s (FD más) | ≈ 40 m @1M … 500 m @125k | Half | Robusto, arbitraje, CRC | 8 B (FD 64), terminación | Vehículos, maquinaria |

**Números clave:** UART 8N1 = 10 bits/byte (115 200 → 11 520 B/s). I2C: `Rmin=(Vcc−0.4)/3 mA`, `Rmax=tr/(0.8473·Cb)`; tr = 1000 ns @100 kHz, 300 ns @400 kHz. CAN: ≈ 60 Ω apagado; recesivo ≈ 2.5 V; dominante CANH≈3.5/CANL≈1.5 V. DS18B20: 12 bits = 0.0625 °C, 750 ms, reset 85 °C, sin sensor −127 °C. → [`docs/02`](docs/02_protocolos_comunicacion.md)

**CAN / CANopen / J1939:** CAN = capas 1–2 · CANopen = aplicación (OD, PDO/SDO, NMT) · J1939 = vehículos pesados (29 bit: prioridad+PGN+SA, 250 kbit/s típico) · ISOBUS = agrícola (sobre J1939). **CAN FD:** 64 B, fase de datos rápida (BRS), un nodo clásico no entiende tramas FD.

## 2. Fórmulas de electrónica
| | |
|---|---|
| Ohm / potencia | `V=IR` · `P=VI=I²R=V²/R` |
| Divisor | `Vout=Vin·R2/(R1+R2)` |
| LED | `R=(Vcc−Vf)/I` |
| ADC | `LSB=Vref/2^N` · `V=cuentas·Vref/(2^N−1)` |
| Nyquist | `fs>2·fmax` (práctico 5–10×) · alias `|fs−f|` |
| RC | `fc=1/(2πRC)` (−20 dB/dec) |
| NTC β | `1/T=1/T0+(1/β)·ln(R/R0)` (K) |
| 4–20 mA | `%=(mA−4)/16·100` · 250 Ω → 1–5 V |
| PWM | `Vprom=duty·Vcc` |
| Regulador lineal | `P=(Vin−Vout)·I` |
| Ruido | promediar N muestras → σ/√N |
| Caída en cable | `ΔV=I·(2·L·ρ/S)` (ρ Cu ≈ 0.0175 Ω·mm²/m) |
| CAN carga | `carga=tramas/s·bits/trama÷bitrate` (128 bits ≈ ext. 8 B) |
→ [`docs/01`](docs/01_fundamentos_electronica.md), [`docs/05`](docs/05_sensores_y_adquisicion.md)

## 3. Sintaxis esencial

### C / C++
```c
#include <stdint.h>  #include <stdbool.h>  #include <stdio.h>
uint8_t  u8; int16_t i16; uint32_t u32; float f;
reg |=  (1u<<n);   reg &= ~(1u<<n);   reg ^= (1u<<n);   (reg>>n)&1u;
reg = (reg & ~MASK) | (val<<SHIFT);            // escribir un campo
volatile uint32_t flag;                         // ISR/hardware: sin atomicidad
const int *p;  int *const q;                    // dato const / puntero const
for (size_t i=0;i<n;++i) {...}
snprintf(buf,sizeof buf,"%d",x);  strtof(s,&end);  // seguro y con detección de error
switch(state){case A: ...; break; default: ...;}
if ((uint32_t)(now-last) >= period) {...}       // sin delay(), tolera desbordamiento
// C++: const T& x · std::optional<T> · template<typename T,size_t N> class RingBuffer · RAII
```
Compilar: `gcc -std=c11 -Wall -Wextra -o prog prog.c` · C++: `g++ -std=c++17 ...` · sanitizers: `-fsanitize=address,undefined`. → [`docs/03`](docs/03_c_cpp.md)

### Python
```python
with open(p, newline="", encoding="utf-8") as f: ...
try: ...  except (ValueError, KeyError) as e: ...  else: ...  finally: ...
[x for x in xs if lo <= x <= hi]         {k: v for ...}         (x for x in xs)
@dataclass(frozen=True) class M: id: str; value: float
json.loads(s) / json.dumps(o)            csv.DictReader(f)
ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1); ser.readline()   # pip install pyserial
r = requests.post(url, json=d, timeout=5); r.raise_for_status()          # pip install requests
time.monotonic()   logging.getLogger("x").exception("msg")
python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```
→ [`docs/04`](docs/04_python.md)

## 4. Comandos Linux esenciales
| Tarea | Comando |
|---|---|
| Navegar/ver | `pwd` `ls -lah` `cd` `cat` `less` `head -n` `tail -f` |
| Buscar | `grep -rni "txt" .` · `find . -name "*.py" -mtime -1` |
| Permisos | `chmod 754 f` · `chown u:g f` · `id` · `sudo usermod -aG dialout $USER` (re-login) |
| Procesos | `ps aux \| grep x` · `top`/`htop` · `kill PID` · `kill -9` (último recurso) |
| Servicios | `systemctl status\|start\|stop\|restart\|enable --now X` · `journalctl -u X -n 50 -f` |
| Red | `ip a` · `ping -c3 h` · `ss -tulpn` · `curl -v url` · `nc -zv h 1883` · `timedatectl` |
| Hardware | `lsusb` · `dmesg \| tail` · `ls -l /dev/ttyUSB* /dev/serial/by-id/` · `i2cdetect -y 1` |
| CAN | `sudo ip link set can0 type can bitrate 250000 listen-only on` · `candump can0` |
| SSH | `ssh u@h` · `ssh-copy-id u@h` · `scp f u@h:/ruta` · `rsync -avz a/ u@h:b/` |
| Disco/mem | `df -h` · `du -sh *` · `free -m` |
| Bash | `set -euo pipefail` · `"$var"` · `$?` · `cmd > f 2>&1` · cron: `*/5 * * * * cmd` |
Grupo del puerto serial: `dialout` (Debian/Ubuntu/Pi OS); en otras distribuciones `uucp`/`tty`: **comprueba con `ls -l`**. → [`docs/08`](docs/08_linux.md)

## 5. OT vs IT
| | OT | IT |
|---|---|---|
| Prioridad | Disponibilidad, seguridad física | Confidencialidad, integridad |
| Vida útil | 15–30 años | 3–5 años |
| Parches | Difíciles | Frecuentes |
| Tiempo real | Crítico | Tolerante |
| Ejemplos | PLC, SCADA, HMI, ECU, gateway | ERP, servidores, dashboards |
**Monitoreo** (leer) ≠ **control** (escribir). Segmenta (VLAN/DMZ), firewall deny-by-default, **solo conexiones salientes**, TLS/VPN, credenciales únicas, ACL por topic. Purdue ≠ ISA-95 ≠ IEC 62443 (niveles / integración funcional / ciberseguridad). MQTT (pub/sub, QoS 0/1/2, LWT, 1883/8883) vs HTTP (petición/respuesta). TCP (fiable) vs UDP (sin garantía). → [`docs/07`](docs/07_redes_ot_it.md), [`docs/11`](docs/11_conectividad_y_telemetria.md)

**Sin Internet:** buffer persistente + `ts` original + backoff + idempotencia `(device_id, seq)` + heartbeat + alerta local.

## 6. Flujo de diagnóstico (de lo simple a lo complejo)
```
1 Alimentación/GND → 2 Conexión física → 3 Configuración (dir/baud/bitrate)
→ 4 Actividad en el bus (analizador) → 5 Software/permisos → 6 Red → 7 Datos/dashboard
```
| Falla | Primer chequeo |
|---|---|
| I2C no detecta | VCC, SDA/SCL ≈ Vcc (pull-ups), dirección, I2C habilitado |
| UART basura | Baud/formato, TX↔RX, GND, loopback |
| CAN mudo | Bitrate, ≈ 60 Ω, 2.5 V, ACK de otro nodo, `candump -e` |
| 1-Wire −127/85 | Pull-up, CRC, esperar 750 ms |
| MCU se reinicia | Brown-out, watchdog, pila, causa de reset |
| Pi sin serial | `lsusb`, `dmesg`, grupo, cable |
| Servicio no inicia | `systemctl status` + `journalctl -u`, ejecutar a mano |
| API inaccesible | `ping`, DNS, `curl -v`, hora/TLS |
| Dashboard vacío | BD → ingesta → consulta → zona horaria |
| Duplicados/timestamps | idempotencia, NTP/RTC, UTC |
→ [`docs/12`](docs/12_diagnostico_y_troubleshooting.md), [`diagrams/troubleshooting_flow.mmd`](diagrams/troubleshooting_flow.mmd)

## 7. Errores frecuentes (los que más se penalizan)
1. Aceptar valores imposibles (−127, 85, 201 °C) sin validar. 2. Confundir resolución con exactitud. 3. Olvidar GND común / nivel 3.3 vs 5 V. 4. I2C sin pull-ups o sin calcular. 5. CAN con terminador en cada nodo. 6. `volatile` ≠ atómico. 7. División entera, variables sin inicializar, `<=` en bucles. 8. Servicios Python sin timeout/logging/reintentos. 9. Hora de llegada como hora de medición. 10. Exponer OT a Internet o diseñar control cuando se pidió monitoreo. 11. Materiales 3D inadecuados (PLA al sol). 12. No declarar supuestos ni qué verificarías en el datasheet.

## 8. Preguntas de entrevista con respuesta de 2–4 líneas
1. **¿Por qué I2C necesita pull-ups?** Open-drain: solo se puede tirar a 0; la resistencia lleva a 1. `Rmax=tr/(0.8473·Cb)`, `Rmin=(Vcc−0.4)/3 mA`.
2. **¿Terminación CAN?** 120 Ω en los dos extremos (no en cada nodo); ≈ 60 Ω medidos con el bus apagado.
3. **¿Cómo se resuelve la contención en CAN?** Arbitraje bit a bit: dominante (0) gana; ID menor = prioridad mayor; el perdedor se retira sin destruir la trama.
4. **UART vs RS-485.** UART = periférico asíncrono; RS-485 = capa eléctrica diferencial multipunto para distancia.
5. **¿Qué es `volatile`?** Evita optimizar accesos a variables cambiadas por hardware/ISR; no da atomicidad.
6. **Polling vs interrupciones.** Polling simple/predecible; interrupción reacciona rápido; híbrido: ISR marca bandera, lazo procesa.
7. **Watchdog.** Reinicia si no se alimenta; se alimenta en el lazo principal tras verificar salud.
8. **¿Qué pasa si se cae Internet?** Buffer persistente con `ts` original, reintentos con backoff, servidor idempotente `(device_id, seq)`.
9. **MQTT vs HTTP.** MQTT pub/sub ligero con QoS y LWT (telemetría continua); HTTP petición/respuesta (lotes/APIs).
10. **OT vs IT.** OT: procesos físicos, disponibilidad y seguridad; IT: datos, confidencialidad; se unen con gateway + DMZ + salida solamente.
11. **Permisos de `/dev/ttyUSB0`.** Añadir al grupo `dialout` (o el que muestre `ls -l`) y re-iniciar sesión.
12. **DS18B20 marca 85 °C.** Valor de reset: lectura sin conversión válida; validar CRC y esperar la conversión.
13. **Material de carcasa exterior.** ASA (UV/temperatura) o PETG en sombra; evitar PLA; paredes ≥ 2.4 mm, sellado y montaje rígido.
14. **CAN vs J1939.** CAN: capas física/enlace; J1939: aplicación con PGN/SPN sobre ID de 29 bits para vehículos pesados.
15. **¿Cómo detectas sensor desconectado?** Valor imposible, CRC/NACK, live-zero (4–20 mA), saturación, congelamiento, tasa de cambio, correlación.

## 9. Checklist antes de una prueba técnica
**Entorno:** [ ] Cámara/micrófono/pantalla compartida probados · [ ] Internet estable + plan B (datos móviles) · [ ] Editor y terminal listos (Python, `gcc`, Git) · [ ] Agua, hoja y lápiz · [ ] Notificaciones apagadas.
**Contenido:** [ ] Repasé tabla de protocolos y fórmulas · [ ] Hice el simulacro de 60 min ([`mock_exam/`](mock_exam/exam_60min.md)) · [ ] Sé explicar el caso realista ([`docs/15`](docs/15_caso_realista_arquitectura.md)) · [ ] Sé mi proyecto de monitoreo ambiental en 2 min (arquitectura, problema, resultado, mejoras) · [ ] Repasé comandos Linux y `systemctl/journalctl` · [ ] Practiqué bits/punteros y un parser en C · [ ] Practiqué respuestas en inglés ([`docs/13`](docs/13_ingles_tecnico.md)).
**Durante:** [ ] Leo todo el enunciado; pido aclaraciones · [ ] Estructuro: supuestos → diseño → riesgos → verificación · [ ] Pienso en voz alta · [ ] Valido entradas y casos límite en el código · [ ] Si no sé algo: "lo verificaría en el datasheet/estándar" · [ ] No inflo mi experiencia (C/CAN/PLC: en formación) · [ ] Dejo 2 min para repasar.
