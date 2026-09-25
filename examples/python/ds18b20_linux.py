#!/usr/bin/env python3
"""
ds18b20_linux.py
Lee todos los DS18B20 de un Raspberry Pi (u otro Linux con el driver w1-therm).

Preparacion en Raspberry Pi:
  1) Habilitar 1-Wire:  sudo raspi-config -> Interface Options -> 1-Wire   (o dtoverlay=w1-gpio en config.txt)
     GPIO4 por defecto, con pull-up de 4.7 kOhm a 3V3 entre DQ y VDD.
  2) Reiniciar. Comprobar:  ls /sys/bus/w1/devices/    -> 28-xxxxxxxxxxxx (uno por sensor)
Cada w1_slave tiene 2 lineas:
  4b 01 4b 46 7f ff 05 10 e1 : crc=e1 YES
  4b 01 4b 46 7f ff 05 10 e1 t=20687
`YES` significa CRC correcto. `t=` esta en milesimas de grado C.

Sin hardware: python ds18b20_linux.py --demo (usa texto de ejemplo).
"""
import argparse
import glob
import os

W1_DIR = "/sys/bus/w1/devices"

DEMO = {
    "28-000000000001": "4b 01 4b 46 7f ff 05 10 e1 : crc=e1 YES\n4b 01 4b 46 7f ff 05 10 e1 t=20687\n",
    "28-000000000002": "50 05 4b 46 7f ff 0c 10 1c : crc=1c YES\n50 05 4b 46 7f ff 0c 10 1c t=85000\n",
    "28-000000000003": "ff ff ff ff ff ff ff ff ff : crc=c9 NO\nff ff ff ff ff ff ff ff ff t=-1000\n",
}


def parse_w1_slave(text: str):
    """Devuelve (temp_c, estado). Estado: ok / crc / reset_85 / sin_sensor."""
    lines = text.strip().splitlines()
    if len(lines) < 2 or not lines[0].strip().endswith("YES"):
        return None, "crc"                                 # CRC malo: descartar
    try:
        milli = int(lines[1].split("t=")[1])
    except (IndexError, ValueError):
        return None, "formato"
    if milli == -1000 or milli == -62000:                  # marcas tipicas de lectura invalida
        return None, "sin_sensor"
    if milli == 85000:                                     # valor de reset del DS18B20
        return milli / 1000.0, "reset_85"                  # se devuelve pero se marca sospechoso
    return milli / 1000.0, "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()

    if args.demo:
        sensors = {k: v for k, v in DEMO.items()}
    else:
        sensors = {}
        for path in sorted(glob.glob(os.path.join(W1_DIR, "28-*"))):     # 28 = codigo de familia del DS18B20
            with open(os.path.join(path, "w1_slave"), encoding="ascii") as f:
                sensors[os.path.basename(path)] = f.read()
        if not sensors:
            print("no se encontraron sensores (revisar 1-Wire habilitado, pull-up y cableado)")
            return

    for sid, text in sensors.items():
        t, status = parse_w1_slave(text)
        print(f"{sid}: {t} C [{status}]")


if __name__ == "__main__":
    main()

# Salida esperada con --demo:
# 28-000000000001: 20.687 C [ok]
# 28-000000000002: 85.0 C [reset_85]
# 28-000000000003: None C [crc]
