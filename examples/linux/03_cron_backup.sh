#!/usr/bin/env bash
# 03_cron_backup.sh
# Automatizacion: comprime y rota logs/datos locales del gateway.
#
# Programar con cron (crontab -e):
#   # min hora dia mes dia_semana comando
#   */5 * * * *  /opt/gateway/02_gateway_health.sh >> /var/log/gateway_health.log 2>&1   # cada 5 minutos
#   0   2 * * *  /opt/gateway/03_cron_backup.sh                                       # todos los dias a las 02:00
# Alternativa moderna: un "timer" de systemd (mejor registro con journalctl).
#
# Trampas de cron: entorno minimo (PATH corto) -> usar rutas absolutas; la salida se pierde si no se redirige.
set -euo pipefail                    # -e: salir ante error, -u: variable no definida es error, pipefail: falla el pipe si falla un tramo

SRC="${1:-/opt/gateway/data}"
DST="${2:-/opt/gateway/backup}"
KEEP_DAYS="${3:-14}"

mkdir -p "$DST"
stamp=$(date +%Y%m%d_%H%M%S)
tar -czf "$DST/data_$stamp.tar.gz" -C "$SRC" .           # -c crear, -z gzip, -f archivo; -C cambia de directorio
echo "backup creado: $DST/data_$stamp.tar.gz ($(du -h "$DST/data_$stamp.tar.gz" | cut -f1))"

# Borrar copias mas viejas que KEEP_DAYS dias. Primero mostrar (-print) para poder verificar.
find "$DST" -name 'data_*.tar.gz' -mtime +"$KEEP_DAYS" -print -delete
