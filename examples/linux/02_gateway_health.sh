#!/usr/bin/env bash
# 02_gateway_health.sh
# Chequeo de salud de un gateway Linux: servicio, disco, memoria, conectividad, ultimo log.
# Sale con codigo 0 si todo esta bien y 1 si algo falla (util para cron/monitoreo).
#
# Uso:  bash 02_gateway_health.sh [servicio] [host_broker] [puerto]
#       bash 02_gateway_health.sh gateway.service broker.ejemplo.local 8883
#
# Comandos ilustrados: systemctl, df, free, ping, nc, journalctl, awk, $?, if, funciones, arreglos.
SERVICE="${1:-gateway.service}"      # ${VAR:-valor}: valor por defecto si no se paso argumento
BROKER="${2:-127.0.0.1}"
PORT="${3:-1883}"
FAIL=0

check() {                            # check "descripcion" comando...   -> imprime OK/FALLA y acumula errores
    local desc="$1"; shift
    if "$@" >/dev/null 2>&1; then echo "[ OK ] $desc"; else echo "[FALLA] $desc"; FAIL=1; fi
}

check "servicio $SERVICE activo"        systemctl is-active --quiet "$SERVICE"
check "DNS/ping al broker $BROKER"      ping -c 1 -W 2 "$BROKER"
check "puerto $PORT accesible"          timeout 3 bash -c "</dev/tcp/$BROKER/$PORT"   # prueba TCP sin nc (bash)

# Uso de disco de / : falla si supera 90 %
use=$(df --output=pcent / | tail -n 1 | tr -dc '0-9')
if [ "${use:-100}" -lt 90 ]; then echo "[ OK ] disco / al ${use}%"; else echo "[FALLA] disco / al ${use}%"; FAIL=1; fi

# Memoria disponible (MB)
avail=$(free -m | awk '/^Mem:/ {print $7}')
echo "[INFO] memoria disponible: ${avail} MB"

# Ultimos errores del servicio (si journalctl existe)
if command -v journalctl >/dev/null; then
    echo "--- ultimas 5 lineas de $SERVICE ---"
    journalctl -u "$SERVICE" -n 5 --no-pager 2>/dev/null || true
fi

exit $FAIL
