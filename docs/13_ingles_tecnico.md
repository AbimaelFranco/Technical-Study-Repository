# 13 · Inglés técnico (nivel intermedio)

> **Resumen ejecutivo (30 s).** Para la prueba necesitas: (1) **vocabulario técnico** (sensor, pull-up, baud rate, firmware, gateway, timeout), (2) **estructuras simples pero precisas** para describir una arquitectura ("The sensor sends data to the gateway over…"), un problema ("The bus hangs when…") y una solución ("I would first check… then…"), y (3) **respuestas cortas y claras** (2–4 frases). No busques frases sofisticadas: **claridad, orden y términos correctos**. Practica en voz alta.

## 1. Glosario español–inglés

### Electrónica
| Español | English |
|---|---|
| voltaje / tensión | voltage |
| corriente | current |
| resistencia | resistor (componente) / resistance (magnitud) |
| condensador | capacitor |
| inductor / bobina | inductor / coil |
| diodo, transistor | diode, transistor |
| tierra / masa | ground (GND) |
| fuente de alimentación | power supply |
| regulador de voltaje | voltage regulator |
| pull-up / pull-down | pull-up / pull-down resistor |
| divisor de voltaje | voltage divider |
| señal analógica / digital | analog / digital signal |
| ruido | noise |
| filtro paso bajo | low-pass filter |
| desacoplo | decoupling (bypass capacitor) |
| corto circuito | short circuit |
| circuito abierto | open circuit |
| fusible | fuse |
| relé | relay |
| placa de circuito impreso | printed circuit board (PCB) |
| esquemático | schematic |
| soldadura / soldar | solder / to solder |
| multímetro, osciloscopio | multimeter, oscilloscope |
| analizador lógico | logic analyzer |
| conector, cable, arnés | connector, cable, wiring harness |
| par trenzado, blindaje | twisted pair, shielding |

### Sensores y adquisición
| Español | English |
|---|---|
| sensor / transductor | sensor / transducer |
| temperatura, presión, vibración | temperature, pressure, vibration |
| acelerómetro | accelerometer |
| corriente (medición) | current sensing (shunt, Hall-effect sensor) |
| resolución | resolution |
| exactitud | accuracy |
| precisión / repetibilidad | precision / repeatability |
| calibración | calibration |
| desviación (offset) / ganancia | offset / gain |
| deriva | drift |
| frecuencia de muestreo | sampling rate |
| aliasing | aliasing |
| conversor analógico-digital | analog-to-digital converter (ADC) |
| lectura fuera de rango | out-of-range reading |
| sensor desconectado | disconnected sensor / open sensor |
| umbral | threshold |
| histéresis | hysteresis |
| valor atípico | outlier |

### Firmware y programación
| Español | English |
|---|---|
| microcontrolador | microcontroller (MCU) |
| firmware | firmware |
| interrupción | interrupt |
| temporizador | timer |
| perro guardián | watchdog (timer) |
| máquina de estados | state machine |
| registro | register |
| máscara de bits | bit mask |
| desbordamiento | overflow |
| puntero | pointer |
| pila / montón | stack / heap |
| fuga de memoria | memory leak |
| depurar / depurador | to debug / debugger |
| compilar / enlazar | to compile / to link |
| hilo / proceso | thread / process |
| excepción | exception |
| bucle | loop |
| bloqueante / no bloqueante | blocking / non-blocking |
| reintento | retry |
| tiempo de espera | timeout |

### Redes y comunicaciones
| Español | English |
|---|---|
| puerto serial | serial port |
| tasa de baudios | baud rate |
| bus | bus |
| maestro / esclavo (o controlador/periférico) | master / slave (or controller / peripheral) |
| dirección | address |
| trama / paquete | frame / packet |
| suma de verificación | checksum |
| terminación | termination |
| enlace / conexión | link / connection |
| pasarela / gateway | gateway |
| servidor, cliente | server, client |
| publicar / suscribirse | to publish / to subscribe |
| intermediario (broker) | broker |
| cortafuegos | firewall |
| segmentación de red | network segmentation |
| zona desmilitarizada | demilitarized zone (DMZ) |
| red privada virtual | virtual private network (VPN) |
| cifrado | encryption |
| latencia, ancho de banda | latency, bandwidth |
| pérdida de paquetes | packet loss |
| almacenar y reenviar | store and forward |
| latido (heartbeat) | heartbeat |

### Troubleshooting y trabajo
| Español | English |
|---|---|
| causa raíz | root cause |
| síntoma | symptom |
| hipótesis | hypothesis |
| reproducir el problema | to reproduce the issue |
| solución temporal | workaround |
| parche | patch |
| reinicio | reboot / restart |
| registro (log) | log |
| alerta | alert |
| mantenimiento preventivo | preventive maintenance |
| tiempo de inactividad | downtime |
| disponibilidad | availability |
| requisitos | requirements |
| entregable | deliverable |
| plazo | deadline |
| revisión de código | code review |

## 2. Frases para explicar una arquitectura
- "The system has **three layers**: field devices, an edge gateway, and a server."
- "The **temperature sensor** is connected to the microcontroller over **1-Wire**."
- "The microcontroller **samples** the sensors every second and **sends** the readings to the gateway over **UART**."
- "The gateway **decodes** the CAN frames, **adds a timestamp**, and **publishes** the data to an MQTT broker."
- "If the internet connection is lost, the gateway **stores the data locally** and **forwards it** when the link is restored."
- "We **separate** the OT network from the IT network using a **firewall** and a **DMZ**."
- "The gateway only makes **outbound connections**, so we don't need to open any inbound ports."
- "The data is **encrypted with TLS**, and each device has its **own credentials**."
- "The dashboard **reads from the database** and shows an **alert** when the temperature exceeds the threshold."
- "This design is **read-only**: it monitors the machine but doesn't control it."

## 3. Frases para describir un problema y proponer una solución
**Describir:**
- "The sensor **returns −127** °C, which usually means it's **disconnected**."
- "**I2C doesn't detect** the device at the expected address."
- "The UART output **is garbled**, so I suspect a **baud rate mismatch**."
- "The microcontroller **keeps rebooting**; it might be a **brown-out** or a **watchdog reset**."
- "The data **reaches the server but doesn't show** on the dashboard."
- "We're seeing **duplicate records** after the network comes back."

**Proponer:**
- "**First**, I would check the power supply and the wiring."
- "**Then**, I would measure the voltage on the SDA and SCL lines. It should be close to the supply voltage when idle."
- "**If** that's fine, I would use a **logic analyzer** to see whether the address gets an **ACK**."
- "**A likely cause** is a missing pull-up resistor."
- "**To prevent** this, we can add **validation** and a **quality flag** to each reading."
- "**I'd make the server idempotent** so retries don't create duplicates."
- "**As a workaround**, we can lower the bus speed while we investigate."

**Incertidumbre honesta (buena en entrevistas):**
- "I haven't worked with **CAN** in a production system, but I understand that it **uses differential signaling and arbitration by ID**."
- "I would **check the datasheet** to confirm that value."
- "I'm not sure about the exact number, but it **depends on** the transceiver and the cable."

## 4. Preguntas técnicas comunes y respuestas modelo

**1. Can you tell me about yourself and your technical experience?**
> "I'm an electronics engineer with experience in **Python, SQL, and data analysis**. In a previous project I built an **environmental monitoring system** with a **Raspberry Pi**, **I2C sensors**, **PostgreSQL**, and a **Django** web app. I also 3D-print with an Ender 3. I'm strengthening my **embedded C/C++** skills and I'm eager to learn more about **CAN and industrial networks**."
*(Ajusta a tu historia real; no afirmes experiencia que no tienes.)*

**2. What is the difference between UART and I2C?**
> "**UART** is **asynchronous** and **point-to-point**: two devices, TX and RX, and both must use the same baud rate. **I2C** is **synchronous**, uses a **shared bus** with **SDA and SCL**, and each device has an **address**. I2C is great for several sensors on one board; UART is simple and common for GPS or debugging."

**3. Why does I2C need pull-up resistors?**
> "Because the lines are **open-drain**. Devices can only **pull the line low**; the pull-up resistors bring it **high** when nobody is driving it."

**4. What is CAN and why is it used in vehicles?**
> "CAN is a **robust serial bus** that uses **differential signaling** on **CAN-High and CAN-Low**. It's **multi-master** with **arbitration by message ID**, and it has **built-in error detection**, so it works well in **noisy environments** like tractors and engines."

**5. Why do we need 120-ohm resistors on a CAN bus?**
> "They **match the cable impedance** and prevent **reflections**. There should be one at **each end** of the bus, so about **60 ohms** across CAN-H and CAN-L when the bus is powered off."

**6. What is the difference between CAN and J1939?**
> "CAN defines the **physical and data link layers**. **J1939** is a **higher-layer protocol** built on CAN for heavy vehicles. It defines how to use the **29-bit identifier**, the **PGNs**, and the meaning of the data."

**7. What does `volatile` mean in C?**
> "It tells the compiler that the variable **can change outside the normal program flow**, like in an **interrupt** or a hardware register, so it must **not optimize away** the reads. But it **doesn't make the access atomic** or thread-safe."

**8. Polling or interrupts?**
> "**Polling** is simple and predictable, good for slow sensors. **Interrupts** react quickly to events like pulses or incoming bytes. I usually keep the ISR **very short**: it **sets a flag** or **stores data in a buffer**, and the main loop does the processing."

**9. What is a watchdog timer?**
> "It's a hardware timer that **resets the microcontroller** if the software doesn't **'feed'** it in time. It helps the system **recover automatically** if the firmware hangs."

**10. How would you design a system that monitors a tractor engine temperature?**
> "I'd use a **temperature sensor** on the engine, read it with a **microcontroller**, **validate** the values, and send them to a **gateway**. The gateway **timestamps** the data and **publishes** it to a server through **MQTT over TLS**. If the connection drops, it **buffers locally** and **resends** later. On the server, I'd store the data in a **time-series database** and create a **dashboard with alerts**."

**11. What happens if the internet connection is lost?**
> "The **edge device keeps working**: it continues **sampling** and **stores data** in a local buffer with the **original timestamps**. When the connection returns, it **sends the backlog** with **retries and backoff**, and the server **ignores duplicates** using a sequence number."

**12. What is the difference between OT and IT?**
> "**OT** controls or monitors **physical processes** and prioritizes **availability and safety**. **IT** manages **data and business systems** and traditionally prioritizes **confidentiality**. In a converged architecture we **connect them carefully** with **segmentation** and **firewalls**."

**13. MQTT or HTTP?**
> "**MQTT** is **publish/subscribe** with a **broker**, lightweight, with **QoS levels**, so it's good for **continuous telemetry** over unreliable links. **HTTP/REST** is **request/response**, simple to integrate and debug. Depending on the case I could use both."

**14. How do you debug a Linux service that doesn't start?**
> "I run **`systemctl status`** and **`journalctl -u`** to see the error. Then I try running the command **manually with the same user**. Usually it's a **path**, **permission**, **missing dependency**, or **environment variable**."

**15. How do you choose a material for a 3D-printed enclosure outdoors?**
> "I'd avoid **PLA** because it **softens with heat**. **PETG** is a good general option, and **ASA** is better for **sun and UV**. I'd also design **wall thickness**, **tolerances**, and **sealing** for **vibration and humidity**."

**16. Tell me about a time you solved a difficult problem.** *(Estructura STAR)*
> "**Situation:** our sensor readings were **intermittent**. **Task:** find the cause. **Action:** I checked **the wiring**, measured the **supply voltage**, and found that **the pull-up value was too high** for the cable length. **Result:** I **replaced it**, and the readings became **stable**."
*(Usa un ejemplo real tuyo.)*

## 5. Vocabulario de reuniones y documentación

**Reuniones:**
| Función | Frase |
|---|---|
| Empezar | "Let's get started." / "The goal of today's meeting is to…" |
| Pedir aclaración | "Could you clarify what you mean by…?" · "Just to confirm, you mean…?" |
| Dar opinión | "In my opinion…" · "I would recommend…" · "One option is…" |
| Discrepar con respeto | "I see your point, but I'm concerned about…" |
| Prioridades | "This is **high priority** because…" · "It's **blocking** the deployment." |
| Estimar | "I estimate it will take **two days**." · "It depends on **the hardware delivery**." |
| Riesgos | "The main **risk** is…" · "A **mitigation** would be…" |
| Acuerdos | "So the **next steps** are…" · "**Action items:**…" · "I'll **follow up** by email." |
| Pedir tiempo | "Let me **check** and get back to you." |
| Cerrar | "Thanks everyone. **Let's wrap up**." |

**Documentación (README / informe técnico):**
| Sección | Expresiones |
|---|---|
| Purpose | "This document describes…" |
| Requirements | "The system **shall/must/should**…" (*shall/must* = obligatorio, *should* = recomendado, *may* = opcional) |
| Architecture | "The **architecture consists of**…" |
| Installation | "**Install** the dependencies with…" · "**Run** the following command:" |
| Usage | "**To start** the service, run…" |
| Known issues | "**Known limitations**" · "**Not yet supported**" |
| Troubleshooting | "**If** you see the error…, **check**…" |
| Changelog | "**Added**, **Changed**, **Fixed**, **Removed**" |
| Commit messages | "Add CAN decoder", "Fix timeout handling", "Update README" |

**Tips de pronunciación y claridad:** habla despacio, usa frases cortas (sujeto + verbo + complemento), repite términos técnicos exactos, y si no entiendes: "Could you repeat that, please?" / "Could you rephrase the question?".

## 6. Mini-práctica (responde en voz alta en menos de 30 s cada una)
1. Explain how a DS18B20 works.
2. Describe the OT/IT boundary in your architecture.
3. What would you check if an I2C sensor doesn't respond?
4. Why do we use a timestamp and a sequence number in each message?
5. Explain what a state machine is and why it helps in firmware.
Respuestas de referencia: los módulos 02, 06, 07, 11.
