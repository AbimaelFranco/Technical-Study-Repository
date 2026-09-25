# Índice general

Navega con enlaces relativos. ⭐ = prioridad alta para la prueba.

## 0. Empezar
- [README](README.md) — propósito, estructura, cómo ejecutar, limitaciones
- [STUDY_PLAN](STUDY_PLAN.md) ⭐ — rutas de 2 horas, 1 día y 1 semana
- [QUICK_REFERENCE](QUICK_REFERENCE.md) ⭐ — hoja de repaso intensivo
- [GLOSSARY](GLOSSARY.md) — siglas y términos
- [REFERENCES](REFERENCES.md) — fuentes y lista de verificación de datasheets

## 1. Módulos de estudio (`docs/`)
| # | Módulo | Contenido clave |
|---|---|---|
| 01 | [Fundamentos de electrónica](docs/01_fundamentos_electronica.md) ⭐ | Ohm, ADC, pull-ups, niveles, ruido, filtros |
| 02 | [Protocolos de comunicación](docs/02_protocolos_comunicacion.md) ⭐⭐⭐ | UART, I2C, 1-Wire, CAN, tabla comparativa, J1939 |
| 03 | [C y C++](docs/03_c_cpp.md) ⭐⭐⭐ | Bits, punteros, `volatile`, buffer, parser, FSM |
| 04 | [Python](docs/04_python.md) ⭐⭐⭐ | Datos, serial, HTTP, servicios, logging |
| 05 | [Sensores y adquisición](docs/05_sensores_y_adquisicion.md) ⭐ | Tipos, calibración, muestreo, plausibilidad |
| 06 | [Sistemas embebidos](docs/06_sistemas_embebidos.md) ⭐⭐ | MCU/SBC, interrupciones, watchdog, FSM |
| 07 | [Redes OT/IT](docs/07_redes_ot_it.md) ⭐⭐⭐ | Purdue, IEC 62443, MQTT/HTTP, seguridad |
| 08 | [Linux](docs/08_linux.md) ⭐⭐⭐ | Permisos, systemd, serial, SSH, bash |
| 09 | [Git](docs/09_git_y_control_versiones.md) | Flujo, conflictos, recuperar versiones |
| 10 | [Esquemáticos y diseño 3D](docs/10_esquematicos_y_diseno_3d.md) ⭐⭐ | Lectura de esquemas, PLA/PETG/ASA, carcasas |
| 11 | [Conectividad y telemetría](docs/11_conectividad_y_telemetria.md) ⭐⭐⭐ | Payload, buffer, idempotencia, series de tiempo |
| 12 | [Diagnóstico y troubleshooting](docs/12_diagnostico_y_troubleshooting.md) ⭐⭐⭐ | 12 escenarios en árbol de decisión |
| 13 | [Inglés técnico](docs/13_ingles_tecnico.md) ⭐ | Glosario, frases, preguntas y respuestas |
| 14 | [Casos prácticos A–D](docs/14_casos_practicos.md) ⭐⭐⭐ | Temperatura, vibración, CAN+gateway, sin conexión |
| 15 | [**Caso realista integral**](docs/15_caso_realista_arquitectura.md) ⭐⭐⭐ | Sensores → MCU → gateway → IT/OT, ruido, fallas, seguridad |

## 2. Diagramas (`diagrams/`)
**Mermaid (obligatorios del temario)**
- [architecture_overview.mmd](diagrams/architecture_overview.mmd) — arquitectura completa de monitoreo
- [protocols_topology.mmd](diagrams/protocols_topology.mmd) — topologías de UART, I2C, 1-Wire, CAN
- [ot_it_architecture.mmd](diagrams/ot_it_architecture.mmd) — niveles/segmentación OT/IT
- [troubleshooting_flow.mmd](diagrams/troubleshooting_flow.mmd) — árbol de diagnóstico general
- [state_machine_firmware.mmd](diagrams/state_machine_firmware.mmd) — máquina de estados del nodo
- [sequence_telemetry.mmd](diagrams/sequence_telemetry.mmd) — secuencia de telemetría con QoS 1

**Mapas mentales y comparativas**
- [mindmaps.md](diagrams/mindmaps.md) — global, protocolos, diagnóstico, OT/IT
- [comparativas.md](diagrams/comparativas.md) — cuadrantes, árboles de decisión, tablas

**Interactivos (archify, abrir en navegador)** — ver [diagrams/README.md](diagrams/README.md)
- [architecture_case.html](diagrams/archify/architecture_case.html)
- [dataflow_sensor_to_dashboard.html](diagrams/archify/dataflow_sensor_to_dashboard.html)
- [lifecycle_firmware.html](diagrams/archify/lifecycle_firmware.html)
- [sequence_offline_recovery.html](diagrams/archify/sequence_offline_recovery.html)

## 3. Ejemplos (`examples/`)
**C** ([carpeta](examples/c))
- [01_temperature_stats.c](examples/c/01_temperature_stats.c) — clasificar temperaturas, promedio/mín/máx, inválidos
- [02_circular_buffer.c](examples/c/02_circular_buffer.c) — buffer circular
- [03_serial_parser.c](examples/c/03_serial_parser.c) — parser de mensajes seriales
- [04_state_machine.c](examples/c/04_state_machine.c) — FSM de monitoreo y `struct Measurement`
- [05_bit_manipulation.c](examples/c/05_bit_manipulation.c) — bits y máscaras
- [06_buggy_code.c](examples/c/06_buggy_code.c) — código defectuoso y corregido
- [nmea_parser.c](examples/c/nmea_parser.c) — GPS por UART (NMEA)
- [ds18b20_decode.c](examples/c/ds18b20_decode.c) — scratchpad y CRC-8 del DS18B20
- [i2c_register_read.c](examples/c/i2c_register_read.c) — lectura de registros I2C (bus simulado)

**C++** ([carpeta](examples/cpp))
- [01_sensor_classes.cpp](examples/cpp/01_sensor_classes.cpp) — clases, `optional`, plantillas, RAII
- [arduino_temp_monitor.ino](examples/cpp/arduino_temp_monitor/arduino_temp_monitor.ino) — sketch Arduino (requiere framework)

**Python** ([carpeta](examples/python))
- [01_filter_out_of_range.py](examples/python/01_filter_out_of_range.py) · [02_sensor_statistics.py](examples/python/02_sensor_statistics.py) · [03_read_csv.py](examples/python/03_read_csv.py) · [04_parse_json.py](examples/python/04_parse_json.py)
- [05_serial_reader.py](examples/python/05_serial_reader.py) · [06_post_to_api.py](examples/python/06_post_to_api.py) · [mock_api_server.py](examples/python/mock_api_server.py)
- [07_timeout_detector.py](examples/python/07_timeout_detector.py) · [08_store_and_forward.py](examples/python/08_store_and_forward.py) · [09_alerts_thresholds.py](examples/python/09_alerts_thresholds.py) · [10_logging_errors.py](examples/python/10_logging_errors.py)
- [can_j1939_decode.py](examples/python/can_j1939_decode.py) · [ds18b20_linux.py](examples/python/ds18b20_linux.py) · [i2c_multisensor.py](examples/python/i2c_multisensor.py) · [vibration_anomaly.py](examples/python/vibration_anomaly.py) · [mqtt_publisher.py](examples/python/mqtt_publisher.py)
- Datos: [data/measurements.csv](examples/python/data/measurements.csv) · Dependencias: [requirements.txt](requirements.txt)

**Linux** ([carpeta](examples/linux))
- [01_serial_setup_check.sh](examples/linux/01_serial_setup_check.sh) · [02_gateway_health.sh](examples/linux/02_gateway_health.sh) · [03_cron_backup.sh](examples/linux/03_cron_backup.sh) · [04_can_socketcan.sh](examples/linux/04_can_socketcan.sh) · [gateway.service](examples/linux/gateway.service)

## 4. Ejercicios y evaluación
- [fundamentals.md](exercises/fundamentals.md) · [protocols.md](exercises/protocols.md) · [programming.md](exercises/programming.md) · [linux.md](exercises/linux.md) · [ot_it.md](exercises/ot_it.md)
- [**question_bank.md**](exercises/question_bank.md) ⭐ — banco de preguntas posibles con respuesta corta
- [answer_key.md](exercises/answer_key.md) — soluciones (no mirar antes de intentar)
- **Simulacro de 60 min:** [exam_60min.md](mock_exam/exam_60min.md) → [solutions.md](mock_exam/solutions.md)

## 5. Recorrido sugerido según tu objetivo
| Objetivo | Ruta |
|---|---|
| "No sé por dónde empezar" | [STUDY_PLAN](STUDY_PLAN.md) → [QUICK_REFERENCE](QUICK_REFERENCE.md) |
| Entender el proyecto completo | [15 Caso realista](docs/15_caso_realista_arquitectura.md) → diagramas archify → [07](docs/07_redes_ot_it.md) |
| Reforzar C embebido | [03](docs/03_c_cpp.md) → [`examples/c`](examples/c) → [programming.md](exercises/programming.md) |
| Dominar los buses | [02](docs/02_protocolos_comunicacion.md) → [protocols.md](exercises/protocols.md) → [12](docs/12_diagnostico_y_troubleshooting.md) |
| Practicar la entrevista | [question_bank](exercises/question_bank.md) → [13 Inglés](docs/13_ingles_tecnico.md) → [mock_exam](mock_exam/exam_60min.md) |
