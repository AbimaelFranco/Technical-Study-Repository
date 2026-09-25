# Glosario

Siglas y términos, en orden alfabético. Se conservan en inglés los términos habituales de la industria. **Ver también** el glosario español–inglés en [`docs/13_ingles_tecnico.md`](docs/13_ingles_tecnico.md).

| Término | Significado | Módulo |
|---|---|---|
| **ACK / NACK** | *Acknowledge / Not acknowledge*: confirmación (o negativa) de recepción (I2C, CAN) | [02](docs/02_protocolos_comunicacion.md) |
| **ACL** | *Access Control List*: lista de reglas de permiso (red/topics) | [07](docs/07_redes_ot_it.md) |
| **ADC / DAC** | *Analog-to-Digital / Digital-to-Analog Converter* | [01](docs/01_fundamentos_electronica.md) |
| **Aliasing** | Frecuencias falsas por muestrear por debajo de 2× la frecuencia máxima | [01](docs/01_fundamentos_electronica.md), [05](docs/05_sensores_y_adquisicion.md) |
| **Arbitraje (CAN)** | Resolución bit a bit de quién transmite; el ID menor gana | [02](docs/02_protocolos_comunicacion.md) |
| **Baud rate** | Símbolos por segundo en un enlace serial (en UART = bits/s) | [02](docs/02_protocolos_comunicacion.md) |
| **Backoff exponencial** | Espera creciente entre reintentos (con *jitter* aleatorio) | [11](docs/11_conectividad_y_telemetria.md) |
| **Bit stuffing** | Bit extra tras 5 bits iguales (CAN) para mantener sincronía | [02](docs/02_protocolos_comunicacion.md) |
| **BOD / Brown-out** | Caída de tensión que reinicia/afecta al MCU | [06](docs/06_sistemas_embebidos.md) |
| **Broker** | Servidor intermediario de MQTT | [07](docs/07_redes_ot_it.md) |
| **Buffer circular (ring buffer)** | Cola de tamaño fijo que da la vuelta | [03](docs/03_c_cpp.md) |
| **CAN / CAN FD** | *Controller Area Network / Flexible Data-rate* | [02](docs/02_protocolos_comunicacion.md) |
| **CANopen** | Protocolo de aplicación sobre CAN (CiA 301) | [02](docs/02_protocolos_comunicacion.md) |
| **CRC** | *Cyclic Redundancy Check*: código de detección de errores | [02](docs/02_protocolos_comunicacion.md) |
| **Checksum** | Suma/XOR de verificación (p. ej. NMEA) | [03](docs/03_c_cpp.md) |
| **DBC** | Archivo que describe mensajes/señales CAN | [02](docs/02_protocolos_comunicacion.md) |
| **Desacople (decoupling)** | Condensador junto a Vcc para filtrar/estabilizar | [01](docs/01_fundamentos_electronica.md) |
| **DMZ** | Zona desmilitarizada entre redes | [07](docs/07_redes_ot_it.md) |
| **DS18B20** | Sensor digital de temperatura 1-Wire | [02](docs/02_protocolos_comunicacion.md) |
| **Edge computing** | Procesar cerca de la fuente (gateway) | [11](docs/11_conectividad_y_telemetria.md) |
| **ECU** | *Engine/Electronic Control Unit* | [02](docs/02_protocolos_comunicacion.md) |
| **ENOB** | *Effective Number Of Bits* de un ADC | [01](docs/01_fundamentos_electronica.md) |
| **ERP / MES / SCADA / HMI / PLC** | Empresa / manufactura / supervisión / interfaz local / controlador | [07](docs/07_redes_ot_it.md) |
| **FSM** | *Finite State Machine* | [06](docs/06_sistemas_embebidos.md) |
| **Footprint** | Patrón de pads de un componente en la PCB | [10](docs/10_esquematicos_y_diseno_3d.md) |
| **GNSS / GPS** | Posicionamiento por satélite | [05](docs/05_sensores_y_adquisicion.md) |
| **GPIO** | *General Purpose Input/Output* | [06](docs/06_sistemas_embebidos.md) |
| **Gateway** | Pasarela entre redes/protocolos | [07](docs/07_redes_ot_it.md) |
| **Heartbeat** | Mensaje periódico que indica que el dispositivo está vivo | [11](docs/11_conectividad_y_telemetria.md) |
| **Histéresis** | Banda entre umbral de disparo y de retorno | [05](docs/05_sensores_y_adquisicion.md) |
| **I2C** | *Inter-Integrated Circuit* | [02](docs/02_protocolos_comunicacion.md) |
| **IEC 62443** | Serie de normas de ciberseguridad industrial | [07](docs/07_redes_ot_it.md) |
| **Idempotencia** | Repetir una operación no cambia el resultado | [11](docs/11_conectividad_y_telemetria.md) |
| **ISA-95** | Modelo de integración empresa-control (IEC 62264) | [07](docs/07_redes_ot_it.md) |
| **ISOBUS (ISO 11783)** | Estándar agrícola basado en CAN/J1939 | [02](docs/02_protocolos_comunicacion.md) |
| **ISR** | *Interrupt Service Routine* | [03](docs/03_c_cpp.md), [06](docs/06_sistemas_embebidos.md) |
| **J1939** | Protocolo SAE para vehículos pesados sobre CAN | [02](docs/02_protocolos_comunicacion.md) |
| **Jitter** | Variación de la latencia/temporización | [07](docs/07_redes_ot_it.md) |
| **Latencia** | Retardo extremo a extremo | [07](docs/07_redes_ot_it.md) |
| **Level shifter** | Adaptador de niveles lógicos (3.3 ⇄ 5 V) | [01](docs/01_fundamentos_electronica.md) |
| **Listen-only** | Modo en que un nodo CAN solo escucha | [02](docs/02_protocolos_comunicacion.md) |
| **LSB** | Bit menos significativo / paso mínimo del ADC | [01](docs/01_fundamentos_electronica.md) |
| **LWT** | *Last Will and Testament* (MQTT) | [07](docs/07_redes_ot_it.md) |
| **MCU / MPU / SBC** | Microcontrolador / microprocesador / computador de placa única | [06](docs/06_sistemas_embebidos.md) |
| **MQTT** | *Message Queuing Telemetry Transport* (pub/sub) | [07](docs/07_redes_ot_it.md) |
| **NTP / RTC** | Protocolo de hora de red / reloj de tiempo real | [11](docs/11_conectividad_y_telemetria.md) |
| **NMEA 0183** | Formato de frases de GPS | [02](docs/02_protocolos_comunicacion.md) |
| **Nyquist** | `fs > 2·fmax` | [01](docs/01_fundamentos_electronica.md) |
| **Open-drain** | Salida que solo tira a 0 | [01](docs/01_fundamentos_electronica.md) |
| **OT / IT** | *Operational / Information Technology* | [07](docs/07_redes_ot_it.md) |
| **Outbox** | Cola persistente de mensajes pendientes | [11](docs/11_conectividad_y_telemetria.md) |
| **PCB** | *Printed Circuit Board* | [10](docs/10_esquematicos_y_diseno_3d.md) |
| **PGN / SPN** | *Parameter Group Number / Suspect Parameter Number* (J1939) | [02](docs/02_protocolos_comunicacion.md) |
| **Pull-up / pull-down** | Resistencia que fija nivel alto/bajo por defecto | [01](docs/01_fundamentos_electronica.md) |
| **Purdue (PERA)** | Modelo de referencia por niveles | [07](docs/07_redes_ot_it.md) |
| **PWM** | *Pulse Width Modulation* | [06](docs/06_sistemas_embebidos.md) |
| **QoS** | *Quality of Service* (MQTT: 0, 1, 2) | [07](docs/07_redes_ot_it.md) |
| **Retain** | Bandera MQTT que conserva el último mensaje del topic | [07](docs/07_redes_ot_it.md) |
| **RMS** | Valor cuadrático medio (indicador de vibración/energía) | [05](docs/05_sensores_y_adquisicion.md) |
| **RS-232 / RS-422 / RS-485** | Capas eléctricas seriales | [02](docs/02_protocolos_comunicacion.md) |
| **RTOS** | *Real-Time Operating System* | [06](docs/06_sistemas_embebidos.md) |
| **SocketCAN** | Interfaz CAN del kernel Linux | [08](docs/08_linux.md) |
| **SPI** | *Serial Peripheral Interface* | [02](docs/02_protocolos_comunicacion.md) |
| **Store & forward** | Guardar localmente y reenviar cuando hay red | [11](docs/11_conectividad_y_telemetria.md) |
| **Terminación** | Resistencia (120 Ω en CAN) que adapta el bus | [02](docs/02_protocolos_comunicacion.md) |
| **TLS** | *Transport Layer Security* | [07](docs/07_redes_ot_it.md) |
| **Transceptor** | Chip que adapta niveles del controlador al medio físico | [02](docs/02_protocolos_comunicacion.md) |
| **TVS** | Diodo supresor de transitorios | [01](docs/01_fundamentos_electronica.md) |
| **UART** | *Universal Asynchronous Receiver/Transmitter* | [02](docs/02_protocolos_comunicacion.md) |
| **UTC** | Tiempo universal coordinado | [11](docs/11_conectividad_y_telemetria.md) |
| **venv** | Entorno virtual de Python | [04](docs/04_python.md) |
| **VPN** | *Virtual Private Network* | [07](docs/07_redes_ot_it.md) |
| **Watchdog** | Temporizador que reinicia el sistema si no se alimenta | [06](docs/06_sistemas_embebidos.md) |
| **1-Wire** | Bus de un hilo de datos (Maxim/Analog Devices) | [02](docs/02_protocolos_comunicacion.md) |
