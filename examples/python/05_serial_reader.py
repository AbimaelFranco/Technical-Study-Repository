#!/usr/bin/env python3
"""
05_serial_reader.py
Programa 5: leer datos de un puerto serial con pySerial.

Instalacion:  pip install pyserial
Uso real:     python 05_serial_reader.py --port /dev/ttyUSB0 --baud 115200        (Linux)
              python 05_serial_reader.py --port COM3 --baud 115200                (Windows)
Sin hardware: python 05_serial_reader.py --demo    (usa el puerto virtual "loop://" de pySerial)

El dispositivo envia una linea JSON por muestra (ver examples/cpp/arduino_temp_monitor).
Puntos clave:
  - timeout en la lectura: read() no se bloquea para siempre.
  - decodificar con errors="replace": el ruido no debe tumbar el programa.
  - lineas parciales/basura se descartan; el arranque suele traer texto del bootloader.
En Linux, el usuario debe pertenecer al grupo del dispositivo (dialout en Debian/Ubuntu/Raspberry Pi OS).
"""
import argparse
import json

import serial  # pyserial (importa como "serial")


def read_lines(ser, max_lines=None):
    """Generador de dicts. `ser.readline()` devuelve b'' si vence el timeout."""
    count = 0
    while max_lines is None or count < max_lines:
        raw = ser.readline()                                  # lee hasta '\n' o timeout
        if not raw:
            yield None                                        # timeout: el llamador decide (ver 07_timeout_detector.py)
            count += 1
            continue
        text = raw.decode("utf-8", errors="replace").strip()  # bytes -> str
        count += 1
        if not text:
            continue
        try:
            yield json.loads(text)
        except json.JSONDecodeError:
            print(f"linea descartada: {text[:60]!r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="loop://")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()

    # serial_for_url acepta rutas reales ("/dev/ttyUSB0", "COM3") y URLs ("loop://")
    ser = serial.serial_for_url(args.port, baudrate=args.baud, timeout=1.0)
    with ser:
        if args.demo or args.port.startswith("loop://"):
            # En loop:// lo escrito se puede leer: simula un dispositivo.
            ser.write(b'boot v1.2\n{"id":"esp-01","seq":1,"temp_c":80.25,"quality":"good"}\n'
                      b'{"id":"esp-01","seq":2,"temp_c":null,"quality":"bad"}\n')
            n = 3
        else:
            n = None
        for msg in read_lines(ser, n):
            if msg is not None:
                print("recibido:", msg)


if __name__ == "__main__":
    main()

# Salida esperada con --demo:
# linea descartada: 'boot v1.2'
# recibido: {'id': 'esp-01', 'seq': 1, 'temp_c': 80.25, 'quality': 'good'}
# recibido: {'id': 'esp-01', 'seq': 2, 'temp_c': None, 'quality': 'bad'}
