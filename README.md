# Technical Study Repository — Ingeniero en Electrónica (Ingenio La Unión)

Repositorio de estudio para preparar una **prueba técnica virtual de 1 hora** para la plaza de **Ingeniero en Electrónica** en **Ingenio La Unión (Guatemala, costa sur)**, cuyo propósito es *diseñar, prototipar e implementar la arquitectura electrónica y de conectividad para el monitoreo en tiempo real de maquinaria agrícola, asegurando la convergencia entre redes OT y sistemas IT*.

> **Idea central:** no leer por leer. Cada tema tiene **resumen de 30–60 s**, diagramas, tablas comparativas, **código ejecutado**, errores frecuentes, preguntas trampa y ejercicios con soluciones. Todo gira alrededor de un **caso realista integral** (monitoreo de temperatura de maquinaria: sensores → MCU → gateway → servidor → dashboard, con IT/OT, protocolos, ruido y fallas).

## Requisitos de la plaza → dónde estudiarlos

| Requisito | Módulo principal | Práctica |
|---|---|---|
| Ingeniería electrónica / mecatrónica | [01 Fundamentos](docs/01_fundamentos_electronica.md), [05 Sensores](docs/05_sensores_y_adquisicion.md), [06 Embebidos](docs/06_sistemas_embebidos.md) | [`fundamentals.md`](exercises/fundamentals.md) |
| C/C++ avanzado | [03 C/C++](docs/03_c_cpp.md) | [`examples/c`](examples/c), [`examples/cpp`](examples/cpp) |
| Python avanzado | [04 Python](docs/04_python.md) | [`examples/python`](examples/python) |
| UART, I2C, 1-Wire, CAN | [02 Protocolos](docs/02_protocolos_comunicacion.md) | [`protocols.md`](exercises/protocols.md) |
| Linux | [08 Linux](docs/08_linux.md) | [`examples/linux`](examples/linux), [`linux.md`](exercises/linux.md) |
| Impresión/diseño 3D, esquemáticos | [10 Esquemáticos y 3D](docs/10_esquematicos_y_diseno_3d.md) | — |
| Convergencia OT/IT, telemetría | [07 OT/IT](docs/07_redes_ot_it.md), [11 Telemetría](docs/11_conectividad_y_telemetria.md) | [`ot_it.md`](exercises/ot_it.md) |
| Diagnóstico | [12 Troubleshooting](docs/12_diagnostico_y_troubleshooting.md) | [14 Casos](docs/14_casos_practicos.md) |
| Inglés intermedio | [13 Inglés técnico](docs/13_ingles_tecnico.md) | Práctica oral |

## Empieza aquí
1. **Con poco tiempo:** [`STUDY_PLAN.md`](STUDY_PLAN.md) (rutas de 2 h, 1 día, 1 semana) y [`QUICK_REFERENCE.md`](QUICK_REFERENCE.md).
2. **Lo más importante para entender el puesto:** [`docs/15_caso_realista_arquitectura.md`](docs/15_caso_realista_arquitectura.md) + los **diagramas interactivos** de [`diagrams/archify/`](diagrams/archify).
3. **Preguntas posibles:** [`exercises/question_bank.md`](exercises/question_bank.md) (banco con respuesta corta) y el **simulacro de 60 min** en [`mock_exam/`](mock_exam/exam_60min.md).
4. **Todo el índice:** [`INDEX.md`](INDEX.md).

## Estructura

```
/
├── README.md · INDEX.md · STUDY_PLAN.md · QUICK_REFERENCE.md · GLOSSARY.md · REFERENCES.md
├── docs/                    Módulos 01-13 (temario) + 14 (casos A-D) + 15 (caso realista)
├── diagrams/
│   ├── *.mmd                Mermaid (renderiza en GitHub): arquitectura, protocolos, OT/IT, troubleshooting, FSM, secuencia
│   ├── mindmaps.md          Mapas mentales
│   ├── comparativas.md      Comparativas visuales y árboles de decisión
│   └── archify/             Diagramas INTERACTIVOS (HTML autocontenido) + su especificación JSON
├── examples/
│   ├── c/  cpp/  python/  linux/   Código comentado y verificado (ver abajo)
├── exercises/               fundamentals · protocols · programming · linux · ot_it · answer_key · question_bank
└── mock_exam/               exam_60min.md · solutions.md
```

## Diagramas: qué hay y cómo verlos
- **Mermaid** (`.mmd` y bloques dentro de los `.md`): GitHub los renderiza directamente; también en https://mermaid.live o en VS Code (extensión Mermaid).
- **archify** (`diagrams/archify/*.html`): abre el archivo en el navegador (doble clic o *Open with Live Server*). Tienen tema claro/oscuro, zoom y paneo, búsqueda, trazado de relaciones y exportación. **GitHub no los ejecuta** (los muestra como texto): descárgalos o clónalo y ábrelos localmente.

| Diagrama interactivo | Qué muestra |
|---|---|
| [`architecture_case.html`](diagrams/archify/architecture_case.html) | Arquitectura del caso realista con zonas OT/IT, buses y buffer |
| [`dataflow_sensor_to_dashboard.html`](diagrams/archify/dataflow_sensor_to_dashboard.html) | Del sensor al dashboard (formato y estado de cada dato) |
| [`lifecycle_firmware.html`](diagrams/archify/lifecycle_firmware.html) | Máquina de estados del firmware |
| [`sequence_offline_recovery.html`](diagrams/archify/sequence_offline_recovery.html) | Pérdida de red y recuperación (store & forward) |

Las especificaciones JSON permiten regenerarlos con el skill *archify* (ver [`diagrams/README.md`](diagrams/README.md)).

## Cómo ejecutar los ejemplos

### Python (≥ 3.9; probado en 3.13)
```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt                        # pyserial, requests (obligatorias para 05 y 06)
cd examples/python
python 01_filter_out_of_range.py
python 02_sensor_statistics.py
python 03_read_csv.py
python 04_parse_json.py
python 05_serial_reader.py --demo                      # puerto virtual loop://, sin hardware
python mock_api_server.py --fail-first 2 &             # terminal 1 (o en otra terminal, sin &)
python 06_post_to_api.py                               # terminal 2
python 07_timeout_detector.py
python 08_store_and_forward.py
python 09_alerts_thresholds.py
python 10_logging_errors.py
python can_j1939_decode.py
python ds18b20_linux.py --demo
python i2c_multisensor.py --demo
python vibration_anomaly.py
```
`mqtt_publisher.py` requiere `paho-mqtt` y un broker (no probado contra un broker real).

### C y C++ (en PC; no requieren hardware)
```bash
cd examples/c
gcc -std=c11 -Wall -Wextra -o temp_stats 01_temperature_stats.c -lm && ./temp_stats
# Repite con: 02_circular_buffer.c 03_serial_parser.c 04_state_machine.c 05_bit_manipulation.c
#             06_buggy_code.c nmea_parser.c ds18b20_decode.c i2c_register_read.c
cd ../cpp && g++ -std=c++17 -Wall -Wextra -o sensors 01_sensor_classes.cpp && ./sensors
```
En Windows puedes usar MSYS2/MinGW, WSL, o `zig cc`/`zig c++` (`pip install ziglang`, luego `python -m ziglang cc ...`). El sketch de Arduino ([`arduino_temp_monitor.ino`](examples/cpp/arduino_temp_monitor/arduino_temp_monitor.ino)) requiere el **framework Arduino** y las bibliotecas OneWire/DallasTemperature, y **no se ejecutó en hardware** en este repositorio.

### Linux (Bash/systemd)
Los scripts de [`examples/linux/`](examples/linux) están pensados para Debian/Ubuntu/Raspberry Pi OS: `bash examples/linux/01_serial_setup_check.sh`, etc. Se verificó la **sintaxis** (`bash -n`); la ejecución completa requiere un Linux real (systemd, `journalctl`, `ip`, `can-utils`).

## Perfil del estudiante y honestidad técnica
El material asume: formación en ingeniería electrónica; experiencia en **Python, SQL, análisis de datos, aplicaciones web y sensores** (Raspberry Pi, I2C, PostgreSQL, Django); conocimientos de impresión 3D (Ender 3); simulaciones básicas de automatización (Zelio Soft). **No** se presenta al estudiante como experto en PLC, CAN o automatización industrial, y su experiencia en firmware C/C++ es menor que en Python: por eso los módulos 02, 03, 06 y 07 son los más detallados. En la entrevista, **di lo que sabes y lo que verificarías**.

## Control de calidad (qué se verificó y qué no)
| Elemento | Verificación realizada |
|---|---|
| Ejemplos C/C++ | Compilados con `zig cc`/`zig c++` (Clang) `-Wall -Wextra`, sin advertencias, **ejecutados**; salidas coinciden con las documentadas |
| Ejemplos Python | **Ejecutados** con Python 3.13 (05 con `pyserial`; 06 con `requests` contra el servidor local); salidas coinciden |
| Scripts Bash / systemd | `bash -n` (sintaxis). **No** ejecutados en Linux con systemd/CAN |
| Diagramas Mermaid | Los **41 bloques** renderizados con `mermaid-cli` (sin errores); aun así, GitHub puede usar otra versión |
| Diagramas archify | Validación `showcase` (0 errores) y comprobación en navegador (1440×900 a 2048×1320, sin desbordes) |
| Cálculos | Verificados con Python (LSB, pull-ups, NTC, divisores, conversiones DS18B20, tráfico, CAN) |
| Enlaces internos | Comprobados con un script (ver historial del repositorio) |
| Referencias externas | Existencia comprobada con HTTP el 2026-09-25; **contenido no revisado línea por línea** ([`REFERENCES.md`](REFERENCES.md)) |
| Hardware real | **No** probado (sin Arduino/CAN/1-Wire físicos) |

## Limitaciones importantes
- **Didáctico, no producción.** Los ejemplos ilustran conceptos. Un diseño industrial requiere validación, análisis de riesgos, cumplimiento normativo y pruebas en campo.
- **No apto para control crítico o seguridad funcional** sin el diseño y la validación correspondientes (IEC 61508/ISO 13849/ISO 25119). El alcance es **monitoreo**.
- **Valores dependientes del contexto** (velocidad y distancia de buses, direcciones I2C, temperaturas de filamentos, umbrales de alarmas, PGN/SPN) son **típicos**: **verifica siempre en el datasheet o estándar**. Lista de control en [`REFERENCES.md`](REFERENCES.md#7-limitaciones-y-qué-verificar-en-datasheets-lista-de-control).
- J1939/ISOBUS: los PGN/SPN de los ejemplos (61444/65262; SPN 190/110) son de uso común pero **confírmalos en SAE J1939-71 o en el DBC del fabricante**.
- Las cifras de tráfico, latencia, energía y costos del caso realista son **supuestos ilustrativos**.

## Licencia
Ver [`LICENSE`](LICENSE).
