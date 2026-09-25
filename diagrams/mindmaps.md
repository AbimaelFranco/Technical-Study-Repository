# Mapas mentales

Repasa cada rama en voz alta: si no puedes explicar un nodo en 20 segundos, vuelve al módulo indicado.

## Mapa global de la plaza

```mermaid
mindmap
  root((Ingeniero Electronica - Ingenio))
    Electronica
      Ley de Ohm
      ADC y muestreo
      Pull-up / pull-down
      Ruido y tierra
    Protocolos
      UART
      I2C
      1-Wire
      CAN
        Clasico vs FD
        J1939 CANopen
    Programacion
      C/C++
        bits y punteros
        volatile
        FSM
      Python
        pySerial
        JSON CSV
        requests
    Linux
      permisos dialout
      systemd journalctl
      SSH
    OT / IT
      Purdue
      MQTT HTTP
      Buffer local
      Seguridad
    Fisico
      Esquematicos
      3D PLA PETG ASA
    Ingles
```

## Mapa de protocolos

```mermaid
mindmap
  root((Protocolos serie))
    UART
      Asincrono
      TX RX GND
      Baudrate acordado
      Punto a punto
      RS-232 RS-485 son capas fisicas
    I2C
      Sincrono
      SDA SCL
      Direcciones 7 bit
      Pull-ups obligatorios
      Maestro multiple posible
    1-Wire
      Un hilo de datos
      ROM 64 bit unica
      Pull-up
      DS18B20
    CAN
      Diferencial CANH CANL
      Multi-maestro
      Arbitraje por ID
      Terminacion 120 ohm
      CRC y ACK
```

## Mapa de diagnóstico

```mermaid
mindmap
  root((Falla))
    Energia
      VCC
      GND comun
      Brownout
    Fisico
      Conector
      Cable
      Terminacion
    Configuracion
      Baudrate
      Direccion
      Bitrate
    Software
      Permisos
      Servicio caido
      Bug
    Red
      DNS
      Firewall
      TLS
    Datos
      Timestamps
      Duplicados
      Unidades
```

## Mapa OT/IT

```mermaid
mindmap
  root((OT / IT))
    OT
      PLC
      SCADA
      HMI
      Disponibilidad primero
    IT
      ERP
      Servidores
      Confidencialidad primero
    Convergencia
      Gateway
      DMZ
      MQTT
      Unidireccional
    Riesgos
      Exponer PLC a Internet
      Credenciales por defecto
      Sin segmentacion
```
