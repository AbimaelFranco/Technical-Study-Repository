#!/usr/bin/env bash
# 01_serial_setup_check.sh
# Diagnostico rapido de un puerto serial USB en Linux (Debian/Ubuntu/Raspberry Pi OS).
# Solo LEE informacion; no modifica nada. Ejecutar:  bash 01_serial_setup_check.sh
#
# Comandos que se usan (memorizalos):
#   lsusb            lista dispositivos USB (identifica FTDI/CH340/CP210x/Arduino)
#   dmesg | tail     mensajes del kernel: "ttyUSB0 attached", errores de enumeracion
#   ls -l /dev/tty{USB,ACM}*   nodos de dispositivo y su grupo (normalmente "dialout" en Debian/Ubuntu/Pi OS;
#                              en otras distribuciones puede ser "uucp" o "tty": verificar con ls -l)
#   groups           grupos del usuario actual
set -u   # error si se usa una variable no definida (buena practica); NO usamos set -e para poder seguir tras un fallo

echo "== Dispositivos USB (lsusb) =="
command -v lsusb >/dev/null && lsusb || echo "(lsusb no instalado: sudo apt install usbutils)"

echo
echo "== Puertos seriales presentes =="
shopt -s nullglob                     # si no hay coincidencias, el glob se expande a nada (no al texto literal)
ports=(/dev/ttyUSB* /dev/ttyACM*)
if [ ${#ports[@]} -eq 0 ]; then
    echo "No hay /dev/ttyUSB* ni /dev/ttyACM*."
    echo "  - Revisar cable (algunos cables USB son solo de carga), puerto, alimentacion."
    echo "  - Ver: dmesg | tail -n 20"
else
    for p in "${ports[@]}"; do
        ls -l "$p"
        grp=$(stat -c %G "$p")        # grupo propietario del dispositivo
        if id -nG | tr ' ' '\n' | grep -qx "$grp"; then
            echo "  OK: el usuario '$USER' pertenece al grupo '$grp'"
        else
            echo "  FALTA permiso: agregar con  sudo usermod -aG $grp $USER   y volver a iniciar sesion"
        fi
    done
fi

echo
echo "== Procesos que usan los puertos (puede requerir sudo) =="
for p in "${ports[@]}"; do
    command -v fuser >/dev/null && fuser -v "$p" 2>&1 || true   # 'fuser' muestra quien tiene abierto el puerto
done

echo
echo "== Ultimos mensajes del kernel sobre USB/serial =="
dmesg 2>/dev/null | grep -Ei 'tty(USB|ACM)|usb .*(error|disconnect)' | tail -n 10 \
  || echo "(sin permiso para dmesg: probar 'sudo dmesg' o 'journalctl -k')"

echo
echo "== Raspberry Pi: UART de hardware =="
ls -l /dev/serial0 /dev/serial1 2>/dev/null || echo "(no es una Raspberry Pi o no hay /dev/serial*)"
