# Ejercicios · Linux

> Soluciones en [`answer_key.md`](answer_key.md) (sección **Linux**). Teoría: [`docs/08_linux.md`](../docs/08_linux.md). Practica en una máquina virtual/Raspberry Pi/WSL; **no** ejecutes comandos destructivos en un sistema real sin entenderlos.

## Nivel básico
**L-B1 (C).** Explica qué hace cada comando: `pwd`, `ls -lah`, `cd ..`, `mkdir -p /opt/gateway/data`, `cp -r`, `mv`, `rm -r`.
**L-B2 (LEC).** Interpreta: `-rwxr-xr-- 1 gateway dialout 4096 Mar 1 10:00 run.sh`. ¿Quién puede hacer qué? ¿Qué número octal es?
**L-B3 (C).** ¿Qué hace `chmod 640 datos.csv`? ¿Y `chmod +x script.sh`?
**L-B4 (C).** ¿Diferencia entre `>` y `>>`? ¿Qué hace `2>&1`?
**L-B5 (C).** ¿Qué es `/dev/ttyUSB0` y en qué se diferencia de `/dev/ttyACM0`?
**L-B6 (MC).** ¿Cuál comando muestra los puertos TCP/UDP en escucha y el proceso que los usa?
a) `ping` b) `ss -tulpn` c) `df -h` d) `journalctl`

## Nivel intermedio
**L-I1 (DEP).** Tu script Python da `PermissionError: /dev/ttyUSB0`. Da el diagnóstico y la solución (con comandos) y menciona la diferencia según distribución.
**L-I2 (DIS).** Escribe los comandos para: ver el estado del servicio `gateway.service`, ver las últimas 50 líneas de su log, seguirlo en vivo y reiniciarlo.
**L-I3 (DIS).** Busca, en `/var/log`, todas las líneas que contengan `ERROR` (ignorando mayúsculas) mostrando el número de línea; y cuenta cuántas hay.
**L-I4 (DIS).** Encuentra archivos `.csv` de más de 100 MB modificados en las últimas 24 h bajo `/opt/gateway`.
**L-I5 (DIS).** Crea un entorno virtual, instala `pyserial` y `requests`, congela las dependencias y ejecútalo.
**L-I6 (C).** ¿Diferencia entre SIGTERM, SIGKILL y SIGINT? ¿Por qué se prefiere SIGTERM?
**L-I7 (DIS).** Escribe una tarea cron que ejecute `/opt/gateway/02_gateway_health.sh` cada 5 minutos, guardando salida y errores en un log. ¿Qué trampas tiene cron?
**L-I8 (DIS).** Copia `datos.csv` a un servidor por SSH, y sincroniza un directorio con `rsync`. ¿Cómo configuras la autenticación por clave?
**L-I9 (LEC).** `journalctl -u gateway` muestra `status=203/EXEC`. ¿Qué significa y qué revisas?

## Nivel avanzado
**L-A1 (DEP).** Un servicio funciona ejecutado a mano pero falla bajo systemd. Enumera 6 diferencias de entorno que lo explican.
**L-A2 (DIS).** Escribe una unidad systemd para un servicio Python con usuario dedicado, acceso al puerto serial, variables desde un archivo, y reinicio automático con espera de 5 s.
**L-A3 (DEP).** El disco se llena y el gateway deja de guardar. Describe el proceso para encontrar qué ocupa el espacio y qué políticas aplicarías (logrotate, límites, alertas).
**L-A4 (DIS).** Escribe un script Bash que verifique: servicio activo, puerto MQTT alcanzable, disco < 90 %, y salga con código ≠ 0 si algo falla. ¿Qué hace `set -euo pipefail`?
**L-A5 (DEP).** Al conectar dos adaptadores USB-serie los nombres `ttyUSB0/1` se intercambian tras reiniciar. ¿Cómo lo haces estable?
**L-A6 (DIS).** Levanta una interfaz CAN a 250 kbit/s en **modo solo escucha** y muestra tramas. ¿Por qué *listen-only*?
**L-A7 (DEP).** `ssh` da `Permission denied (publickey)`. Da 5 causas y pruebas.
**L-A8 (C).** ¿Por qué `sudo pip install` es mala idea en Raspberry Pi OS / Debian recientes? ¿Qué es PEP 668?

## Práctica guiada
1. Ejecuta `bash examples/linux/01_serial_setup_check.sh` con y sin un adaptador USB-serie.
2. Instala `examples/linux/gateway.service` en una VM (ajustando rutas), rómpelo a propósito (ruta incorrecta) y diagnostica con `systemctl status` + `journalctl`.
3. Usa `vcan0` (`modprobe vcan`) para practicar `candump`/`cansend` sin hardware.
