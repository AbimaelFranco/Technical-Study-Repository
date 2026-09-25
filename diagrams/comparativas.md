# Comparativas visuales

> Hojas de comparación para **decidir y recordar**. Las posiciones en los gráficos son **cualitativas y didácticas** (no medidas): dependen de transceptor, cable, configuración y software. Verifica cifras en datasheets/estándares.

## 1. Protocolos: complejidad vs robustez/alcance (cualitativo)

```mermaid
quadrantChart
    title Protocolos serie (posicion cualitativa)
    x-axis "Simple de usar" --> "Mas complejo"
    y-axis "Corto alcance / poco robusto" --> "Largo alcance / robusto"
    quadrant-1 "Robusto y complejo"
    quadrant-2 "Robusto y simple"
    quadrant-3 "Simple y limitado"
    quadrant-4 "Complejo y limitado"
    "I2C": [0.35, 0.15]
    "UART TTL": [0.15, 0.25]
    "1-Wire": [0.25, 0.4]
    "RS-485": [0.45, 0.8]
    "CAN": [0.7, 0.85]
    "CANopen / J1939": [0.9, 0.9]
```

## 2. Elegir un bus en 5 preguntas

```mermaid
flowchart TD
    A["Que necesito conectar?"] --> B{"Distancia > 1-2 m<br/>o entorno ruidoso?"}
    B -- No --> C{"Un solo dispositivo<br/>punto a punto?"}
    C -- Si --> UART["UART"]
    C -- No --> D{"Muchos sensores lentos<br/>de temperatura?"}
    D -- Si --> OW["1-Wire (DS18B20)"]
    D -- No --> I2C["I2C (o SPI si necesito velocidad)"]
    B -- Si --> E{"Multiples nodos que hablan<br/>entre si / vehiculo / maquinaria?"}
    E -- Si --> CAN["CAN (J1939 / ISOBUS en agricola)"]
    E -- No --> R485["RS-485 (Modbus RTU maestro-esclavo)"]
```

## 3. MCU vs SBC: qué usar para cada rol

| Rol | Arduino/AVR | ESP32 | STM32 | RP2040 (Pico) | Raspberry Pi |
|---|---|---|---|---|---|
| Nodo sensor simple | ✔ | ✔ | ✔ | ✔ | ✘ excesivo |
| Nodo inalámbrico | ✘ | ✔ | (con módulo) | Pico W | ✔ |
| Tiempo real estricto | ✔ | ✔ | ✔ (más recursos) | ✔ | ✘ (Linux estándar) |
| CAN nativo (con transceptor) | ✘ (MCP2515 SPI) | ✔ (TWAI) | ✔ (bxCAN/FDCAN) | ✘ (MCP2515) | (HAT/USB-CAN) |
| ADC | 10 bits | 12 bits (no lineal) | 12 bits (mejor) | 12 bits | ✘ (externo) |
| Gateway / base de datos / Python | ✘ | limitado (MicroPython) | ✘ | limitado | ✔ |
| Costo/complejidad | Bajo | Bajo | Medio | Bajo | Medio |

## 4. MQTT vs HTTP/REST

| Criterio | MQTT | HTTP/REST |
|---|---|---|
| Patrón | Publicar/suscribir | Petición/respuesta |
| Overhead | Muy bajo | Mayor (cabeceras) |
| Conexión | Persistente | Por petición (o keep-alive) |
| Tiempo real hacia el cliente | Sí (push) | No (polling/WebSocket) |
| Redes inestables | Excelente (QoS, LWT, sesión) | Requiere lógica propia |
| Depuración | Herramientas MQTT | `curl`, navegador |
| Integración con sistemas existentes | Menor | Mayor |
| Idóneo para | Telemetría continua | Lotes, consultas, APIs |

## 5. Estrategias de envío

| Estrategia | Datos/día | Latencia | Complejidad | Cuándo |
|---|---|---|---|---|
| Periódica 1 Hz | Alta (≈ 30 MB/máquina con 350 B/msg) | Baja | Baja | Poco tráfico permitido |
| Agregada 5 s | ≈ 6 MB | Media | Media | Enlace celular |
| Por excepción (deadband) | Variable, muy baja | Baja | Media | Variables estables |
| Por lotes (HTTP) | Media | Alta | Baja | Sin necesidad de tiempo real |
*(Cálculo del módulo [15](../docs/15_caso_realista_arquitectura.md); supuestos ilustrativos.)*

## 6. Materiales de impresión 3D (orientativo)

```mermaid
xychart-beta
    title "Temperatura de ablandamiento aproximada (C) - verificar filamento"
    x-axis [PLA, PETG, ABS, ASA]
    y-axis "C" 40 --> 120
    bar [58, 75, 100, 100]
```

| | PLA | PETG | ABS | ASA |
|---|---|---|---|---|
| Facilidad | ★★★★★ | ★★★★ | ★★ | ★★ |
| Calor | ★ | ★★ | ★★★★ | ★★★★ |
| UV/exterior | ★ | ★★ | ★★ | ★★★★★ |
| Impacto | ★ | ★★★★ | ★★★ | ★★★ |
| Recomendado para | Prototipos | Uso general | Interior moderado | **Exterior/sol** |

## 7. Ruido y mitigación: mapa de decisión

```mermaid
flowchart LR
    N["Ruido en la medicion"] --> T{"Tipo?"}
    T -- "Alta frecuencia en Vcc" --> A["Desacople 100 nF + 10 uF, buen GND"]
    T -- "Acoplado por cables" --> B["Par trenzado, blindaje, separar de potencia, 4-20 mA"]
    T -- "Lazo de tierra" --> C["Tierra en un punto, blindaje a un extremo, aislamiento"]
    T -- "Picos de arranque/alternador" --> D["TVS, DC/DC automotriz, filtro LC, fusible"]
    T -- "Ruido aleatorio en el ADC" --> E["Promedio / mediana, filtro RC, Vref estable"]
    T -- "Aliasing" --> F["Filtro anti-aliasing + fs correcta"]
```

## 8. Linux: qué comando para qué síntoma

| Síntoma | Comando |
|---|---|
| ¿Corre el servicio? | `systemctl status X` |
| ¿Por qué falló? | `journalctl -u X -n 100` |
| ¿Está el dispositivo? | `lsusb`, `dmesg \| tail`, `ls -l /dev/ttyUSB*` |
| ¿Permisos? | `ls -l`, `id`, `groups` |
| ¿Puerto en uso? | `ss -tulpn`, `fuser -v` |
| ¿Red? | `ip a`, `ping`, `curl -v`, `nc -zv` |
| ¿Disco/memoria? | `df -h`, `free -m` |
| ¿Hora? | `timedatectl` |
| ¿Bus I2C/CAN? | `i2cdetect -y 1`, `candump can0` |
