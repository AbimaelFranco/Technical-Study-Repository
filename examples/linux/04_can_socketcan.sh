#!/usr/bin/env bash
# 04_can_socketcan.sh
# Levantar una interfaz CAN con SocketCAN y observar el bus (Linux con adaptador CAN o HAT MCP2515).
# Requiere: paquete can-utils (sudo apt install can-utils) e iproute2.
#
# SEGURIDAD: en maquinaria real usa modo LISTEN-ONLY para no transmitir ni confirmar (ACK) tramas.
# Enviar tramas a un bus de vehiculo sin conocer sus consecuencias puede causar movimientos peligrosos.
#
# Uso: sudo bash 04_can_socketcan.sh can0 250000
IFACE="${1:-can0}"
BITRATE="${2:-250000}"        # J1939/ISOBUS: 250000 típicamente; el bitrate DEBE coincidir con el del bus

set -e
ip link set "$IFACE" down 2>/dev/null || true
ip link set "$IFACE" type can bitrate "$BITRATE" listen-only on   # solo escuchar
ip link set "$IFACE" up
ip -details -statistics link show "$IFACE"     # estado: ERROR-ACTIVE/PASSIVE/BUS-OFF, contadores de errores

echo "Escuchando 10 s (Ctrl+C para cortar)..."
timeout 10 candump "$IFACE" || true            # muestra tramas: interfaz  ID  [DLC]  datos
# Ejemplo de linea:   can0  0CF00400   [8]  FF FF FF D0 39 FF FF FF
# Filtrar por ID:     candump can0,0CF00400:1FFFFFFF
# Guardar/reproducir: candump -l can0   |   canplayer -I archivo.log
# Sin hardware, interfaz virtual:  sudo modprobe vcan; sudo ip link add dev vcan0 type vcan; sudo ip link set up vcan0
