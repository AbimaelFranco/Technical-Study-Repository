# Banco de preguntas posibles (con respuesta corta)

> **Cómo usarlo.** (1) Tapa la respuesta y contesta en voz alta en ≤ 30 s. (2) Marca ✅/❌. (3) Repasa las ❌ en el módulo indicado. Las respuestas son de **2–4 líneas**, como en una entrevista; si necesitas profundizar, ve al módulo.
> **Leyenda de prioridad:** ⭐⭐⭐ muy probable · ⭐⭐ probable · ⭐ posible. Los temas ⭐⭐⭐ corresponden a requisitos **explícitos** de la plaza (UART, I2C, 1-Wire, CAN, C/C++, Python, Linux, OT/IT, esquemáticos, 3D).
> **Honestidad técnica:** tu perfil es fuerte en Python/datos y sensores I2C con Raspberry Pi; en C embebido, CAN y automatización industrial estás en formación. Si no sabes algo, di qué verificarías (datasheet/estándar) en vez de inventar.

---

## A. Electrónica básica

**A1 ⭐⭐⭐ Ley de Ohm y potencia.** `V = I·R`; `P = V·I = I²R = V²/R`. Ej.: 12 V sobre 470 Ω → 25.5 mA, 0.31 W. [`01`](../docs/01_fundamentos_electronica.md)

**A2 ⭐⭐⭐ ¿Qué es un divisor de voltaje y para qué lo usas?** `Vout = Vin·R2/(R1+R2)`. Adaptar 12 V/5 V a un ADC de 3.3 V, leer batería; considerar impedancia y tolerancias.

**A3 ⭐⭐⭐ Pull-up vs pull-down.** Resistencias que fijan un nivel por defecto (1 o 0) cuando nadie maneja la línea; evitan entradas flotantes.

**A4 ⭐⭐⭐ ¿Qué es la resolución de un ADC y cómo se calcula el LSB?** `LSB = Vref/2^N`. 12 bits, 3.3 V → 0.806 mV.

**A5 ⭐⭐⭐ Resolución vs exactitud.** Resolución = mínimo cambio detectable; exactitud = cercanía al valor real. Un ADC de 16 bits ruidoso puede ser menos exacto que uno de 12 bits bueno.

**A6 ⭐⭐⭐ Teorema de Nyquist y aliasing.** `fs > 2·fmax`; sin filtro anti-aliasing, componentes por encima de fs/2 aparecen como frecuencias falsas (700 Hz a 1 kHz → 300 Hz).

**A7 ⭐⭐ ¿Cómo eliminas ruido en una señal analógica?** Desacople (100 nF), filtro RC, blindaje/par trenzado, tierra en un punto, promedio/mediana digital, señal diferencial o 4–20 mA.

**A8 ⭐⭐ ¿Qué es un lazo de tierra?** Diferencia de potencial entre dos puntos de masa que hace circular corriente por el blindaje/señal → ruido. Mitigar con masa en un solo punto o aislamiento galvánico.

**A9 ⭐⭐ ¿Por qué un condensador de desacople junto al pin de alimentación del CI?** Aporta corriente instantánea y filtra picos de alta frecuencia que causarían caídas de Vcc y ruido.

**A10 ⭐⭐⭐ ¿Puedo conectar 5 V a un GPIO de 3.3 V?** No (puede dañarlo): divisor/level shifter, y verificar si el pin es 5 V-tolerant en el datasheet.

**A11 ⭐⭐ ¿Qué es open-drain?** La salida solo puede tirar a 0; el nivel 1 lo pone una pull-up externa; permite compartir la línea (I2C, 1-Wire) sin cortocircuito.

**A12 ⭐⭐ ¿Por qué se usa 4–20 mA en industria?** Inmune al ruido y a caída de tensión por cable largo, y 0 mA indica cable roto (*live zero*).

**A13 ⭐⭐ ¿Cómo manejas una carga inductiva (relé/motor) con un GPIO?** Transistor/MOSFET/driver + diodo de rueda libre; el GPIO no debe manejar la corriente directamente.

**A14 ⭐ ¿Regulador lineal o buck?** Lineal: simple/silencioso pero disipa `(Vin−Vout)·I`; buck: eficiente con más ruido de conmutación. 12→3.3 V a 200 mA: 1.74 W en un lineal.

**A15 ⭐⭐ ¿Qué es PWM y qué controla?** Señal con duty variable; controla potencia media (`V_prom = duty·Vcc`): brillo, velocidad de motor DC, servo; con RC actúa como DAC.

---

## B. Protocolos (UART, I2C, 1-Wire, CAN)

**B1 ⭐⭐⭐ UART vs I2C: diferencias.** UART: asíncrono, punto a punto, TX/RX, baud acordado. I2C: síncrono, bus con SDA/SCL, direcciones de 7 bits, pull-ups. [`02`](../docs/02_protocolos_comunicacion.md)

**B2 ⭐⭐⭐ ¿Cómo es una trama UART 8N1?** Start (0) + 8 bits LSB primero + stop (1) = 10 bits por byte; en reposo la línea está en 1.

**B3 ⭐⭐⭐ ¿Qué pasa si el baud rate no coincide?** Se muestrea mal y aparecen caracteres corruptos. Se comprueba con osciloscopio (ancho de bit = 1/baud) y loopback.

**B4 ⭐⭐ UART vs RS-232 vs RS-485.** UART es el periférico/protocolo; RS-232 (±V, punto a punto) y RS-485 (diferencial, multipunto, largas distancias) son capas eléctricas.

**B5 ⭐⭐⭐ ¿Por qué I2C necesita pull-ups y cómo las calculas?** Open-drain. `Rmin = (Vcc−0.4)/3 mA`; `Rmax = tr/(0.8473·Cb)`. 3.3 V, 400 kHz, 200 pF → 1 kΩ–1.8 kΩ.

**B6 ⭐⭐⭐ ¿Cómo funciona el direccionamiento I2C?** El maestro envía START + dirección de 7 bits + R/W; el esclavo responde ACK. Conflicto de direcciones → pin ADDR, multiplexor (TCA9548A) u otro bus.

**B7 ⭐⭐ Velocidades de I2C.** Estándar 100 kbit/s, Fast 400, Fast-plus 1 Mbit/s, High-speed 3.4 Mbit/s; el límite real depende de capacitancia, pull-ups y dispositivos.

**B8 ⭐⭐ ¿Qué es clock stretching?** El esclavo mantiene SCL bajo para pedir más tiempo. El maestro debe soportarlo.

**B9 ⭐⭐⭐ `i2cdetect` no muestra el dispositivo: ¿qué haces?** Alimentación → pull-ups (SDA/SCL ≈ Vcc) → cableado/dirección → I2C habilitado → analizador lógico (¿ACK?) → aislar dispositivos, bajar velocidad.

**B10 ⭐⭐ ¿Qué es un bus I2C atascado y cómo se libera?** Un esclavo mantiene SDA en 0 tras un reinicio a medio byte; se envían hasta 9 pulsos de SCL y un STOP, o se reinicia el esclavo.

**B11 ⭐⭐⭐ ¿Cómo funciona 1-Wire y cuál es su ventaja?** Un solo hilo de datos + GND, ROM de 64 bits única por dispositivo (Search/Match/Skip ROM); muchos sensores en un cable (DS18B20).

**B12 ⭐⭐⭐ ¿Qué significa −127 °C y 85 °C en un DS18B20?** −127: sensor desconectado/bus en alto; 85: valor de reset (lectura sin conversión). Siempre validar CRC.

**B13 ⭐⭐ Resolución y tiempo de conversión del DS18B20.** 9–12 bits (0.5–0.0625 °C); conversión hasta ~750 ms a 12 bits (verificar el datasheet).

**B14 ⭐⭐ Modo parásito vs alimentación normal.** Parásito: VDD a GND y energía por DQ (necesita strong pull-up); alimentación normal es más fiable en cables largos.

**B15 ⭐⭐⭐ ¿Qué es CAN y por qué se usa en vehículos?** Bus diferencial multi-maestro con arbitraje por ID, detección de errores (CRC, ACK, bit stuffing) y gran inmunidad al ruido.

**B16 ⭐⭐⭐ ¿Dónde van las resistencias de 120 Ω y cuánto mides?** Una en cada extremo del bus (no en cada nodo). Con el bus apagado ≈ 60 Ω entre CANH y CANL.

**B17 ⭐⭐⭐ ¿Cómo funciona el arbitraje CAN?** Bit a bit; el dominante (0) gana al recesivo (1). ID menor = prioridad mayor; el perdedor se retira sin destruir la trama del ganador.

**B18 ⭐⭐⭐ CAN clásico vs CAN FD.** Clásico: hasta 8 B y bitrate único (≤ 1 Mbit/s). FD: hasta 64 B y fase de datos más rápida (BRS); nodos clásicos no entienden tramas FD.

**B19 ⭐⭐⭐ CAN vs CANopen vs J1939.** CAN: capas 1–2. CANopen: aplicación (diccionario de objetos, PDO/SDO, NMT). J1939: aplicación para vehículos pesados (29 bit: prioridad+PGN+SA). ISOBUS (ISO 11783): agricultura, sobre J1939.

**B20 ⭐⭐ ¿Qué es un PGN y un SPN?** PGN: grupo de parámetros identificado en el ID de 29 bits; SPN: parámetro concreto dentro de los datos (p. ej. SPN 190 = velocidad del motor). Consultar SAE J1939-71/DBC.

**B21 ⭐⭐⭐ ¿Qué transceptor necesita CAN en un MCU?** El controlador CAN da TX/RX lógicos; un transceptor (TJA1051, SN65HVD230…) genera CANH/CANL. Protocolo ≠ interfaz física ≠ transceptor.

**B22 ⭐⭐ Velocidad vs longitud en CAN.** A mayor velocidad, menor longitud (retardo de propagación); orientativo: 1 Mbit/s ≈ 40 m, 125 kbit/s ≈ 500 m; depende de cable, transceptor y topología.

**B23 ⭐⭐⭐ CAN no comunica: ¿qué revisas?** Bitrate, terminación (≈ 60 Ω apagado), voltajes en reposo (~2.5 V), CANH/CANL, alimentación del transceptor, que exista otro nodo que dé ACK, `candump -e`/osciloscopio.

**B24 ⭐⭐ Estados de error de un nodo CAN.** Error Active → Error Passive (contador > 127) → Bus-Off (> 255), con contadores TEC/REC.

**B25 ⭐⭐ ¿Por qué *listen-only* al conectar a un tractor?** No transmite ni da ACK: evita alterar el bus y comportamientos peligrosos.

**B26 ⭐⭐ ¿Qué es bit stuffing?** Inserción de un bit opuesto tras 5 bits iguales para mantener la sincronización; 6 iguales = error.

**B27 ⭐⭐ ¿Qué diferencia hay entre SPI e I2C?** SPI: 4 hilos (SCLK, MOSI, MISO, CS), full-duplex, más rápido, sin direcciones (CS por dispositivo). I2C: 2 hilos con direcciones, más lento.

**B28 ⭐ Modbus RTU vs CAN.** Modbus RTU: maestro-esclavo sobre RS-485, simple, direcciones de esclavo; CAN: multi-maestro con arbitraje por ID.

---

## C. C / C++

**C1 ⭐⭐⭐ ¿Qué hace `volatile`?** Impide que el compilador optimice/cachee accesos a una variable que puede cambiar fuera del flujo (ISR/hardware). **No** da atomicidad ni sincronización entre hilos. [`03`](../docs/03_c_cpp.md)

**C2 ⭐⭐⭐ ¿Cómo pones/quitas/inviertes/lees un bit?** `|= (1u<<n)`, `&= ~(1u<<n)`, `^= (1u<<n)`, `(x>>n)&1u`.

**C3 ⭐⭐⭐ ¿Diferencia entre puntero y referencia?** Puntero: puede ser nulo y reasignarse; referencia (C++): alias no nulo fijo. C no tiene referencias.

**C4 ⭐⭐⭐ Stack vs heap.** Stack: variables locales, automático, rápido, limitado (overflow); heap: `malloc/new`, manual, fragmentación y no determinista; en MCU se evita en el lazo periódico.

**C5 ⭐⭐⭐ ¿Qué significa `const int *p` vs `int *const p`?** Dato constante vs puntero constante.

**C6 ⭐⭐⭐ Paso por valor vs por referencia.** Valor: copia (no modifica el original); referencia/puntero: accede al original y evita copias grandes.

**C7 ⭐⭐ ¿Por qué usar `uint8_t/uint16_t/uint32_t`?** Tamaño fijo y portable (`int` varía entre plataformas); esencial para registros y protocolos.

**C8 ⭐⭐ ¿Qué es la promoción entera?** Los tipos pequeños se promueven a `int` en expresiones: `uint8_t a=200,b=100; a+b` = 300; al guardar en `uint8_t` = 44.

**C9 ⭐⭐ ¿Qué es un buffer circular y por qué se usa?** Cola de tamaño fijo con índices head/tail que dan la vuelta; O(1), sin heap; típico entre ISR y lazo principal.

**C10 ⭐⭐ ¿Cómo evitas `delay()` bloqueante?** `if (now - last >= period)` con `millis()`; la aritmética `uint32_t` tolera el desbordamiento.

**C11 ⭐⭐ ISR: buenas prácticas.** Cortas, sin `printf`/`malloc`, solo marcan banderas/copian datos; variables compartidas `volatile` y acceso atómico.

**C12 ⭐⭐ ¿Qué es una máquina de estados y por qué en firmware?** Modelo de estados y transiciones; comportamiento predecible, testeable, no bloqueante.

**C13 ⭐⭐ ¿Qué es un dangling pointer?** Puntero a memoria ya liberada o fuera de ámbito (p. ej. devolver dirección de una variable local).

**C14 ⭐⭐ Errores de compilación vs linking.** Compilación: sintaxis/tipos/declaraciones. Linking: `undefined reference` (falta definir/enlazar) o `multiple definition`.

**C15 ⭐⭐ ¿Qué diferencia C y C++ en embebido?** C++ añade clases, templates, RAII, `constexpr`; en MCU se usa con moderación (sin excepciones/RTTI/heap dinámico).

**C16 ⭐⭐ Endianness.** Orden de bytes: little-endian (LSB primero, ARM/x86) vs big-endian (redes, muchos sensores). Serializar explícitamente.

**C17 ⭐ ¿Qué es el padding en un `struct`?** Bytes de alineación que agrega el compilador; no serialices structs crudos.

**C18 ⭐⭐ ¿Cómo validas la entrada de un parser serial?** Longitud, checksum, formato numérico (`strtof` con `end`), rangos, buffer acotado, resincronización.

**C19 ⭐ ¿Qué es RAII?** Adquirir recursos en el constructor y liberarlos en el destructor (cierre garantizado); ej. un puerto serial en una clase.

**C20 ⭐⭐ ¿Por qué la comparación `float == float` es peligrosa?** Errores de redondeo; comparar con tolerancia (excepto centinelas exactos).

---

## D. Python

**D1 ⭐⭐⭐ Lista, tupla, diccionario y set.** Ordenada mutable / ordenada inmutable (hashable) / clave→valor / únicos sin orden. [`04`](../docs/04_python.md)

**D2 ⭐⭐⭐ ¿Qué problema tiene `def f(x, acc=[])`?** El valor por defecto mutable se crea una vez y se comparte entre llamadas; usar `None`.

**D3 ⭐⭐⭐ ¿Cómo manejas datos inválidos de un sensor?** Validar tipo/rango/NaN, excepciones propias, registrar y continuar, marcar `quality`, no descartar en silencio.

**D4 ⭐⭐⭐ ¿Por qué `with open(...)`?** Cierra el archivo aunque haya excepción.

**D5 ⭐⭐⭐ ¿Cómo lees un puerto serial?** `pyserial`: `serial.Serial(port, baud, timeout=1)`, `readline()`, `decode(errors="replace")`, manejar `SerialException` y permisos.

**D6 ⭐⭐⭐ ¿Cómo envías datos a una API REST?** `requests.post(url, json=data, timeout=5)`, verificar `status_code`, reintentos con backoff solo en errores transitorios, idempotencia.

**D7 ⭐⭐⭐ Script vs servicio de larga duración.** El servicio no debe morir: captura errores, logging rotado, señales, reinicio con systemd, sin fugas.

**D8 ⭐⭐ `time.time()` vs `time.monotonic()`.** `monotonic` no salta con cambios de reloj: úsalo para intervalos/timeouts.

**D9 ⭐⭐ ¿Cómo detectas pérdida de comunicación?** Timestamp del último dato por dispositivo (monotonic) y umbral de silencio; heartbeat.

**D10 ⭐⭐ ¿Qué es una dataclass?** Clase para datos con `__init__/__repr__/__eq__` generados; `frozen=True` para inmutable.

**D11 ⭐⭐ ¿Por qué usar `logging` y no `print`?** Niveles, timestamps, destinos múltiples, rotación, `exception()` con traceback.

**D12 ⭐⭐ ¿Entorno virtual: qué es y por qué?** Aislar dependencias por proyecto (`python -m venv`), reproducibilidad con `requirements.txt`.

**D13 ⭐⭐ ¿Cómo guardas datos si no hay red?** Cola persistente (SQLite) escrita antes de enviar; borrar solo tras confirmación; reintentos + idempotencia.

**D14 ⭐ ¿Qué es el GIL y cuándo importa?** Solo un hilo ejecuta bytecode a la vez; no impide paralelismo de E/S; para CPU pura usa procesos/extensiones.

**D15 ⭐⭐ ¿Cómo parseas y validas JSON?** `json.loads` con manejo de `JSONDecodeError`, chequeo de campos/tipos, `datetime.fromisoformat`.

---

## E. Sensores y adquisición

**E1 ⭐⭐⭐ ¿Cómo eliges un sensor de temperatura?** Rango, exactitud, tiempo de respuesta, interfaz, entorno (vibración, humedad), costo: DS18B20 (digital), PT100 (exacto), termopar K (alta T), NTC (barato/no lineal).

**E2 ⭐⭐⭐ ¿Cómo detectas un sensor desconectado?** Valores imposibles (−127), CRC/NACK, live-zero (< 4 mA), saturación, valor congelado, tasa de cambio imposible.

**E3 ⭐⭐⭐ ¿Qué es la calibración?** Corregir offset/ganancia comparando con una referencia trazable (1–2 puntos); registrar coeficientes y fecha.

**E4 ⭐⭐ ¿Cómo mides vibración?** Acelerómetro (MEMS/IEPE) montado rígido; muestreo ≥ 5–10× la banda; indicadores RMS, pico, cresta, espectro.

**E5 ⭐⭐ ¿Cómo mides RPM?** Sensor Hall/inductivo → contar pulsos con interrupción/timer; o leer la ECU por CAN (SPN 190).

**E6 ⭐⭐ ¿Cómo mides corriente?** Shunt + amplificador, sensor Hall (aislado) o CT (solo AC).

**E7 ⭐⭐⭐ ¿Qué consideras al montar sensores en maquinaria?** Vibración (conectores bloqueados, montaje rígido), humedad/polvo (IP), temperatura, EMI, protección eléctrica y facilidad de mantenimiento.

**E8 ⭐⭐ ¿Filtrar más siempre es mejor?** No: agrega retardo y oculta eventos; ajustar al fenómeno.

---

## F. Sistemas embebidos

**F1 ⭐⭐⭐ MCU vs MPU vs SBC.** MCU: CPU+memoria+periféricos en un chip, tiempo real, bajo consumo. MPU: solo CPU (necesita memoria externa). SBC: placa completa con Linux (Raspberry Pi). [`06`](../docs/06_sistemas_embebidos.md)

**F2 ⭐⭐⭐ Raspberry Pi vs Arduino vs ESP32.** Pi: Linux, gateway, sin ADC, no tiempo real duro; Arduino: MCU simple; ESP32: MCU con Wi-Fi/BT, 12 bits ADC (no lineal), dos núcleos.

**F3 ⭐⭐⭐ Polling vs interrupciones.** Polling: simple/predecible; interrupciones: respuesta rápida a eventos. Híbrido: ISR marca bandera y el lazo procesa.

**F4 ⭐⭐⭐ ¿Qué es un watchdog?** Temporizador que reinicia el MCU si no se "alimenta"; se alimenta en el lazo principal tras verificar salud.

**F5 ⭐⭐ ¿Qué es un timer y para qué?** Contador de hardware: periodos, captura de pulsos, PWM, timeouts.

**F6 ⭐⭐ ¿Cómo diseñas firmware robusto?** Autoprueba, timeouts, validación, watchdog, estados degradados, sin heap dinámico, versionado, logs, reintentos acotados.

**F7 ⭐⭐ El MCU se reinicia continuamente: ¿causas?** Brown-out, watchdog, stack overflow, HardFault, ISR mala, ruido en reset; leer la causa del reset y medir Vcc.

**F8 ⭐⭐ ¿Cómo manejas tareas periódicas?** Super-loop con `millis()`, planificador cooperativo por tick, o RTOS.

**F9 ⭐⭐ ¿Qué problemas trae la SD de la Raspberry Pi?** Corrupción ante cortes de energía; usar eMMC/SSD, solo lectura + overlay, escrituras por lotes, UPS.

**F10 ⭐ ¿Qué es un RTOS y cuándo?** Sistema con tareas, prioridades y primitivas (colas/semáforos); útil con varias tareas concurrentes con tiempos.

---

## G. Linux

**G1 ⭐⭐⭐ ¿Cómo lees permisos `-rwxr-xr--`?** dueño rwx, grupo r-x, otros r-- (754). `chmod`, `chown`. [`08`](../docs/08_linux.md)

**G2 ⭐⭐⭐ `PermissionError` en `/dev/ttyUSB0`.** Añadir el usuario al grupo del dispositivo (`dialout` en Debian/Ubuntu/Pi OS; puede ser `uucp`/`tty` en otras) y reiniciar sesión.

**G3 ⭐⭐⭐ ¿Cómo ves el estado y logs de un servicio?** `systemctl status X`, `journalctl -u X -n 50 -f`.

**G4 ⭐⭐⭐ ¿Diferencia entre `ttyUSB0` y `ttyACM0`?** USB-serie (FTDI/CH340/CP210x) vs CDC-ACM (Arduino Uno R3, Pico).

**G5 ⭐⭐⭐ ¿Cómo buscas texto y archivos?** `grep -rni "texto" ruta`, `find ruta -name "*.py" -mtime -1`; tuberías `|`.

**G6 ⭐⭐ ¿Cómo instalas dependencias Python?** `python3 -m venv .venv`, `source .venv/bin/activate`, `pip install -r requirements.txt` (no `sudo pip`; PEP 668).

**G7 ⭐⭐ SSH y transferencia.** `ssh user@host`, claves `ed25519` + `ssh-copy-id`, `scp`/`rsync`.

**G8 ⭐⭐ ¿Qué muestran `ps`, `top`, `ss`, `dmesg`?** Procesos, uso de CPU/memoria en vivo, sockets/puertos, mensajes del kernel (USB, errores de hardware).

**G9 ⭐⭐ Servicio que funciona a mano pero no con systemd.** Usuario, entorno/PATH, `WorkingDirectory`, grupos (dialout), rutas, `After=`.

**G10 ⭐⭐ ¿Cómo automatizas tareas?** `cron` (`*/5 * * * *`), timers de systemd, scripts Bash con `set -euo pipefail`.

**G11 ⭐ ¿Diferencia SIGTERM/SIGKILL?** SIGTERM permite cierre limpio; SIGKILL mata sin aviso.

**G12 ⭐⭐ ¿Cómo estabilizas nombres de puertos seriales?** `/dev/serial/by-id/` o reglas udev.

---

## H. OT/IT, redes y telemetría

**H1 ⭐⭐⭐ ¿Qué es OT y qué es IT? Diferencias.** OT controla procesos físicos (disponibilidad, seguridad, ciclo de vida largo); IT maneja datos (confidencialidad, actualización frecuente). [`07`](../docs/07_redes_ot_it.md)

**H2 ⭐⭐⭐ PLC, SCADA, HMI, MES, ERP.** PLC: control cíclico; SCADA: supervisión/adquisición; HMI: interfaz local; MES: ejecución de producción; ERP: gestión empresarial.

**H3 ⭐⭐⭐ Monitoreo vs control.** Monitoreo lee; control escribe/actúa. Control exige safety, validación y autenticación; el proyecto empieza en monitoreo.

**H4 ⭐⭐⭐ ¿Qué es un gateway y edge computing?** Traduce protocolos, valida, bufferiza y procesa localmente; funciona sin nube; reduce tráfico y riesgo.

**H5 ⭐⭐⭐ MQTT vs HTTP.** MQTT: pub/sub con broker, ligero, QoS, LWT, conexión persistente. HTTP: petición/respuesta, simple e universal.

**H6 ⭐⭐⭐ QoS de MQTT.** 0: a lo más una; 1: al menos una (puede duplicar); 2: exactamente una (más costoso).

**H7 ⭐⭐⭐ TCP vs UDP.** TCP fiable y ordenado con conexión; UDP sin garantía y baja latencia.

**H8 ⭐⭐⭐ ¿Qué ocurre cuando se pierde Internet?** Buffer local persistente, timestamps originales, reintentos con backoff, envío ordenado, idempotencia, alerta local.

**H9 ⭐⭐⭐ ¿Cómo evitas duplicados?** Clave `(device_id, seq)` y `INSERT … ON CONFLICT DO NOTHING`; QoS 1 puede duplicar.

**H10 ⭐⭐⭐ ¿Qué campos lleva un mensaje de telemetría?** `device_id`, `ts` UTC de medición, `seq`, `sensor`, `value`, `unit`, `quality` (+ `schema`, `fw`).

**H11 ⭐⭐⭐ ¿Riesgos de conectar OT directo a Internet?** Servicios expuestos, credenciales por defecto, protocolos sin cifrado, ransomware, manipulación de comandos, sin parches. Mitigar: DMZ, firewall, VPN/TLS, salida solamente.

**H12 ⭐⭐ ¿Purdue, ISA-95, IEC 62443?** Purdue: niveles de referencia; ISA-95: integración funcional empresa-control; IEC 62443: ciberseguridad industrial (zonas y conductos). Complementarios, no equivalentes.

**H13 ⭐⭐ ¿Qué es una DMZ y una VPN?** DMZ: zona intermedia entre redes; VPN: túnel cifrado y autenticado.

**H14 ⭐⭐ ¿Heartbeat y LWT?** Heartbeat: mensaje periódico de vida; LWT: mensaje que el broker publica si el cliente cae sin desconectar.

**H15 ⭐⭐ ¿Con qué frecuencia envías?** Depende de la dinámica del fenómeno, del uso y del costo: periódica, por excepción, agregada, por lotes; alarmas inmediatas.

**H16 ⭐⭐ ¿Dónde guardas series de tiempo?** PostgreSQL/TimescaleDB (SQL), InfluxDB; SQLite local como buffer; políticas de retención/downsampling.

**H17 ⭐⭐ Datos en el servidor pero no en el dashboard.** Verificar BD → ingesta → consulta del panel → zona horaria/filtros/caché.

**H18 ⭐⭐ ¿Cómo aseguras un gateway?** Sin puertos entrantes, TLS, credenciales únicas, ACL, VPN + SSH por clave, secretos fuera del código, actualizaciones controladas.

**H19 ⭐ ¿Por qué UTC?** Evita ambigüedades de zona/horario de verano; se convierte al mostrar.

**H20 ⭐⭐ ¿Qué es idempotencia?** Repetir la operación produce el mismo resultado; base de los reintentos seguros.

---

## I. Esquemáticos, diseño 3D y documentación

**I1 ⭐⭐⭐ ¿Cómo lees un esquemático?** Propósito → alimentación y tierras → entradas/salidas → flujo de señal → pasivos críticos (pull-ups, terminación, desacople) → niveles. [`10`](../docs/10_esquematicos_y_diseno_3d.md)

**I2 ⭐⭐⭐ Esquemático vs PCB vs modelo 3D.** Conexiones lógicas / geometría y pistas / forma física.

**I3 ⭐⭐ ¿Footprint vs encapsulado?** Patrón de pads en la PCB vs cuerpo físico del componente (SOIC-8, 0603…).

**I4 ⭐⭐⭐ PLA vs PETG vs ABS/ASA.** PLA fácil pero se ablanda (~55–60 °C) y no aguanta UV; PETG intermedio; ABS/ASA aguantan calor, ASA mejor en UV; más difíciles de imprimir. Verificar el datasheet del filamento.

**I5 ⭐⭐⭐ ¿Qué consideras al diseñar una carcasa para maquinaria?** Material, tolerancias, orientación de capas, espesor de pared, estanqueidad, vibración, salida de cable, montaje y mantenimiento.

**I6 ⭐⭐ ¿Cómo orientas una pieza impresa para que resista?** Cargas a lo largo de las capas (no entre capas), más perímetros que relleno, filetes en esquinas.

**I7 ⭐⭐ ¿Holgura para encajes?** Aproximadamente 0.2–0.4 mm por lado; imprimir una prueba de tolerancias con tu impresora.

---

## J. Git

**J1 ⭐⭐⭐ Git vs GitHub.** VCS local/distribuido vs plataforma de alojamiento y colaboración. [`09`](../docs/09_git_y_control_versiones.md)

**J2 ⭐⭐⭐ `fetch` vs `pull`.** `fetch` descarga; `pull` = `fetch` + integrar.

**J3 ⭐⭐ ¿Cómo resuelves un conflicto?** Editar marcadores, decidir, `git add`, `git commit`/`rebase --continue`, probar.

**J4 ⭐⭐ ¿Cómo deshaces un commit publicado?** `git revert` (no reescribe historia); `reset --hard` solo en local.

**J5 ⭐⭐ ¿Qué va en `.gitignore`?** Entornos, binarios, logs, datos locales y **secretos**.

---

## K. Experiencia y comportamiento

**K1 ⭐⭐⭐ Cuéntame sobre tu proyecto de monitoreo ambiental.** Estructura: objetivo, arquitectura (Raspberry Pi + sensores I2C + PostgreSQL + Django), tu rol, un problema real y cómo lo resolviste, resultados y qué mejorarías (buffer, validación, alertas).

**K2 ⭐⭐⭐ ¿Qué tanta experiencia tienes con C/C++ y CAN?** Honesto: fundamentos y práctica principalmente en Python; en C/embebido estoy reforzando; CAN lo entiendo conceptualmente y he practicado decodificación/simulación; puedo aprender rápido y verifico en datasheets.

**K3 ⭐⭐ ¿Has trabajado con PLC?** Simulaciones básicas de automatización (Zelio Soft); no me presento como experto en PLC industriales.

**K4 ⭐⭐ Un problema difícil que resolviste (STAR).** Situación, tarea, acción (método: medir, aislar), resultado y aprendizaje.

**K5 ⭐⭐ ¿Cómo aprendes una tecnología nueva rápido?** Datasheet/estándar → ejemplo mínimo en banco → medir → documentar → iterar.

**K6 ⭐⭐ ¿Cómo priorizarías el trabajo el primer mes?** Entender el proceso y la maquinaria, mapear variables críticas, prototipo en 1 máquina, medir/validar, luego escalar.

**K7 ⭐⭐ ¿Disponibilidad y trabajo en campo?** Lunes a viernes en la costa sur; vehículo propio y licencia (requisitos de la plaza); seguridad en campo (EPP, procedimientos).

**K8 ⭐ ¿Por qué esta plaza?** Une electrónica, software y campo: monitoreo real de maquinaria, convergencia OT/IT.

---

## L. Inglés (respuestas breves)

**L1 ⭐⭐ "Explain UART vs I2C."** "UART is asynchronous and point-to-point; I2C is synchronous, uses SDA and SCL, and supports multiple devices with addresses."

**L2 ⭐⭐ "What would you check if the sensor doesn't respond?"** "First the power and wiring, then pull-ups and address, then I'd use a logic analyzer to look for the ACK."

**L3 ⭐⭐ "Describe your monitoring architecture."** "Sensors feed a microcontroller; a gateway timestamps and buffers the data and publishes it over MQTT with TLS to a server that stores it and shows a dashboard."

**L4 ⭐⭐ "What if the internet goes down?"** "The gateway stores data locally and forwards it when the link returns; the server ignores duplicates."

**L5 ⭐ "Tell me about yourself."** Ver [`13`](../docs/13_ingles_tecnico.md), pregunta 1 (ajusta a tu experiencia real).

---

## M. Preguntas trampa (¡ojo!)
1. "¿Un ADC de 16 bits mide con 16 bits de exactitud?" → No.
2. "¿`volatile` hace la variable atómica?" → No.
3. "¿Cada nodo CAN lleva su resistencia de 120 Ω?" → No, solo los dos extremos.
4. "¿85 °C del DS18B20 es una temperatura real?" → Puede ser el valor de reset.
5. "¿MQTT QoS 2 elimina los duplicados de mi sistema?" → No del todo: reinicios y reenvíos de aplicación; diseña idempotente.
6. "¿Puedo controlar el motor desde el dashboard?" → No sin análisis de riesgos, safety y validación.
7. "¿Raspberry Pi para control de tiempo real duro?" → No es lo indicado (Linux estándar).
8. "¿Puedo enchufar la salida de 5 V de un Arduino a la Pi?" → No, 3.3 V no tolera 5 V.
9. "¿`chmod 777` soluciona los permisos del puerto serial?" → Mala práctica; usa el grupo correcto.
10. "¿Con más filtrado siempre mejora la medición?" → No, añade retardo.
11. "¿IEC 62443 y el modelo Purdue son lo mismo?" → No.
12. "¿La hora de llegada al servidor sirve como hora de medición?" → No.
13. "¿UART tiene direcciones?" → No.
14. "¿I2C sirve para 10 m?" → No de forma fiable; usa CAN/RS-485.
15. "¿El PLA sirve para la carcasa en el sol del tractor?" → No, se ablanda.
