# Referencias

> **Transparencia sobre la verificación.**
> - Las cifras y afirmaciones de los módulos provienen de conocimiento técnico general y de los ejemplos ejecutados en este repositorio. **No se leyó cada documento enlazado aquí**: las fuentes son para que **tú contrastes** antes de usar un valor en un diseño o responder con precisión.
> - La columna **Estado del enlace** indica solo que la URL **respondió** al ser consultada con `curl` el **2026-09-25** (`200` = respondió; otros códigos = ver nota). No garantiza que el contenido haya sido revisado línea por línea.
> - Los estándares de pago (ISO, IEC, SAE) **no** se pueden leer completos gratis; se enlaza la página oficial del organismo. Cuando el estándar no está disponible, contrasta con notas de aplicación de fabricantes (TI, NXP, Microchip, Bosch).
> - Regla del repositorio: si dudas de un valor, **verifica en el datasheet/estándar** y dilo en la entrevista.

## 1. Protocolos de comunicación

| Tema respaldado | Fuente | URL | Estado (2026-09-25) |
|---|---|---|---|
| **I2C** (UM10204: modos, direcciones, cálculo de pull-ups, t_r, C_b) | NXP, *I²C-bus specification and user manual* | Buscar **"UM10204"** en https://www.nxp.com (el enlace directo `nxp.com/docs/en/user-guide/UM10204.pdf` devolvió **404**; NXP reorganiza su sitio) | ⚠ enlace directo roto; buscar por código |
| **1-Wire / DS18B20** (resolución, tiempos, ROM 64 bits, valor de reset 85 °C, scratchpad, CRC) | Analog Devices (Maxim), *DS18B20 datasheet* | https://www.analog.com/media/en/technical-documentation/data-sheets/DS18B20.pdf | ⚠ no verificable desde la red usada (timeout); buscar "DS18B20 datasheet" en analog.com |
| **1-Wire en Linux** (driver `w1-therm`, `w1_slave`) | Documentación del kernel | https://www.kernel.org/doc/html/latest/w1/index.html | ✅ 200 |
| **CAN** (capa física y enlace) | ISO 11898-1 (enlace) y 11898-2 (capa física de alta velocidad) | https://www.iso.org/standard/63648.html (11898-1) | ✅ 200 (página del estándar; texto de pago) |
| **CAN: requisitos de capa física, terminación** | Texas Instruments, *SLLA270 – Controller Area Network Physical Layer Requirements* | https://www.ti.com/lit/an/slla270/slla270.pdf | ✅ 200 |
| **SocketCAN** (Linux, `can-utils`, `ip link … type can`) | Documentación del kernel | https://www.kernel.org/doc/html/latest/networking/can.html | ✅ 200 |
| **CAN en ESP32** (TWAI) | Espressif ESP-IDF | https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/twai.html | ✅ 200 |
| **CANopen** (CiA 301) | CAN in Automation | https://www.can-cia.org/ (navegar a CANopen; el enlace profundo probado dio 404) | ✅ 200 (portada) |
| **SAE J1939** (PGN/SPN, 29 bit) | SAE International | https://www.sae.org/standards/j1939 | ✅ 200 |
| **ISOBUS (ISO 11783)** | AEF / ISOBUS | https://www.isobus.net/isobus/ | ✅ 200 |
| **Modbus** (RTU/TCP) | Modbus Organization | https://modbus.org/ | ✅ 200 (portada) |
| **NMEA 0183** (frases GPS) | NMEA | https://www.nmea.org/nmea-0183.html | ✅ 200 (especificación de pago) |

## 2. Lenguajes y herramientas

| Tema | Fuente | URL | Estado |
|---|---|---|---|
| Python (lenguaje y biblioteca estándar) | Documentación oficial | https://docs.python.org/3/ | ✅ 200 |
| `logging.handlers` (RotatingFileHandler) | Python docs | https://docs.python.org/3/library/logging.handlers.html | ✅ 200 |
| `sqlite3` | Python docs | https://docs.python.org/3/library/sqlite3.html | ✅ 200 |
| PEP 668 (entornos "externally managed") | Python | https://peps.python.org/pep-0668/ | ✅ 200 |
| pySerial | Documentación oficial | https://pyserial.readthedocs.io/en/latest/ | ✅ 200 |
| Requests | Documentación oficial | https://requests.readthedocs.io/en/latest/ | ✅ 200 |
| C (referencia del lenguaje y biblioteca) | cppreference | https://en.cppreference.com/w/c | ✅ 200 |
| C++ (referencia) | cppreference | https://en.cppreference.com/w/cpp | ✅ 200 |
| Arduino (framework: `Serial`, `millis`, …) | Arduino | https://www.arduino.cc/reference/en/ | ✅ 200 |
| Git | Documentación oficial | https://git-scm.com/doc | ✅ 200 |
| Bash | GNU | https://www.gnu.org/software/bash/manual/bash.html | ✅ 200 |
| `systemctl` / systemd | freedesktop.org | https://www.freedesktop.org/software/systemd/man/systemctl.html | ⚠ respondió 418 a `curl` (bloqueo anti-bots); revisar en navegador o con `man systemctl` |
| Raspberry Pi (configuración, GPIO, interfaces) | Raspberry Pi | https://www.raspberrypi.com/documentation/ | ✅ 200 |
| KiCad (esquemáticos y PCB) | KiCad | https://docs.kicad.org/ | ✅ 200 |
| Mermaid (diagramas) | Mermaid | https://mermaid.js.org/ | ✅ 200 |

## 3. Telemetría, redes y datos

| Tema | Fuente | URL | Estado |
|---|---|---|---|
| **MQTT 3.1.1** (QoS, retain, LWT, keep-alive) | OASIS | https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html | ✅ 200 |
| **MQTT 5.0** | OASIS | https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html | ✅ 200 |
| Broker Mosquitto | Eclipse Mosquitto | https://mosquitto.org/documentation/ | ✅ 200 |
| **HTTP** (semántica, métodos, códigos de estado) | IETF RFC 9110 | https://www.rfc-editor.org/rfc/rfc9110 | ✅ 200 |
| PostgreSQL | Documentación oficial | https://www.postgresql.org/docs/current/ | ✅ 200 |
| TimescaleDB (series de tiempo) | Timescale | https://docs.timescale.com/ | ✅ 200 |
| Docker (opcional para probar brokers/BD) | Docker | https://docs.docker.com/ | ✅ 200 |

## 4. Automatización industrial y ciberseguridad OT

| Tema | Fuente | URL | Estado |
|---|---|---|---|
| **ISA/IEC 62443** (serie de normas de ciberseguridad industrial; zonas y conductos) | ISA | https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards | ✅ 200 |
| **ISA-95** (integración empresa-control; la versión IEC es IEC 62264) | ISA | https://www.isa.org/standards-and-publications/isa-standards/isa-95-standard | ✅ 200 |
| **NIST SP 800-82 Rev. 3** (Guía de seguridad de OT) | NIST | https://csrc.nist.gov/pubs/sp/800/82/r3/final | ✅ 200 |
| Recursos de seguridad de sistemas de control industrial | CISA | https://www.cisa.gov/topics/industrial-control-systems | ✅ 200 |
| **Modelo Purdue (PERA)** | Se describe en ISA-95 y en las guías anteriores (NIST SP 800-82, ISA). No existe una norma única; **no se afirma equivalencia con IEC 62443** | — | — |

## 5. Sensores, componentes y materiales (consultar al fabricante)
- **DS18B20, BME280, MPU-6050, ADS1115, TCA9548A, TJA1050/TJA1051, SN65HVD230, MCP2515, MAX3232, SP3485**: usa el **datasheet del fabricante** (Analog Devices/Maxim, Bosch, TDK InvenSense, Texas Instruments, NXP, Microchip, Semtech/Sipex). Las direcciones I2C y valores citados en el repositorio son **típicos** y deben confirmarse en tu módulo.
- **Filamentos (PLA, PETG, ABS, ASA)**: fichas técnicas (TDS) del fabricante del filamento que uses (temperatura de deflexión/Tg, resistencia UV, condiciones de impresión). Los valores de `docs/10` son **órdenes de magnitud** genéricos.
- **Normas de conectores, IP (IEC 60529), EMC, ATEX y seguridad funcional (IEC 61508, ISO 13849, ISO 25119)**: consultar a los organismos y a los requisitos del ingenio; no se tratan aquí.

## 6. Cómo se verificó el código de este repositorio
- **C/C++** compilado con `zig cc`/`zig c++` (Clang), `-std=c11`/`-std=c++17 -Wall -Wextra`, sin advertencias tras las correcciones, y **ejecutado** con las salidas indicadas.
- **Python 3.13**: los ejemplos se ejecutaron; 05 con `pyserial` (`loop://`), 06 con `requests` contra el servidor local `mock_api_server.py`.
- **Bash**: verificación de sintaxis con `bash -n`; ejecución parcial en Git Bash de Windows (sin systemd/Linux real).
- **No ejecutados en hardware ni contra un broker real:** `arduino_temp_monitor.ino`, `mqtt_publisher.py`, `i2c_multisensor.py` (solo `--demo`), `ds18b20_linux.py` (solo `--demo`), `04_can_socketcan.sh`, `gateway.service`.
- Diagramas **archify**: validados con el chequeo `showcase` (9 comprobaciones, 0 errores) y entregados como HTML; los **41 bloques Mermaid** se renderizaron sin errores con `@mermaid-js/mermaid-cli` (navegador Edge) el 2026-09-25; GitHub puede usar otra versión de Mermaid, así que si algún bloque falla allí, pruébalo en https://mermaid.live. `quadrantChart` y `xychart-beta` (en `diagrams/comparativas.md`) requieren un Mermaid reciente.

## 7. Limitaciones y qué verificar en datasheets (lista de control)
- [ ] Niveles lógicos y tolerancia a 5 V por pin (MCU y sensores).
- [ ] Rango de alimentación, corriente y temperatura de operación de cada sensor.
- [ ] Direcciones I2C reales y pines de dirección; velocidades soportadas.
- [ ] Tiempos de conversión y resolución (DS18B20, ADC).
- [ ] Bitrate y PGN/SPN del tractor (manual del fabricante/DBC).
- [ ] Transceptor CAN: velocidad máxima, modo *listen-only*, alimentación 3.3/5 V, aislamiento.
- [ ] Umbrales de temperatura de motores (fabricante) — los de los ejemplos son ilustrativos.
- [ ] Rango real de temperatura y UV de tu filamento; IP de la carcasa con el conjunto completo.
- [ ] Ediciones vigentes de ISA-95/IEC 62443/J1939/ISO 11898.
- [ ] Políticas de seguridad y TI del ingenio; regulación local de datos y de instalación eléctrica.
