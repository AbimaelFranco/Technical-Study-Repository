#!/usr/bin/env python3
"""
03_read_csv.py
Programa 3: leer un CSV de mediciones (data/measurements.csv), validar cada fila y resumir.

Formato del CSV:  timestamp,device_id,sensor,value,unit
Ejecutar: python 03_read_csv.py [ruta.csv]     (libreria estandar)
"""
import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

DEFAULT = Path(__file__).parent / "data" / "measurements.csv"


def read_measurements(path):
    """Generador: devuelve dicts validados y cuenta las filas malas. Usa `with` para cerrar el archivo."""
    bad = 0
    with open(path, newline="", encoding="utf-8") as f:
        for lineno, row in enumerate(csv.DictReader(f), start=2):     # start=2: la fila 1 es el encabezado
            try:
                yield {
                    "ts": datetime.fromisoformat(row["timestamp"]),
                    "device": row["device_id"].strip(),
                    "sensor": row["sensor"].strip(),
                    "value": float(row["value"]),                       # ValueError si esta vacio o es texto
                    "unit": row["unit"].strip(),
                }
            except (KeyError, ValueError) as e:
                bad += 1
                print(f"fila {lineno} descartada: {e!r}", file=sys.stderr)
    print(f"filas malas: {bad}", file=sys.stderr)


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    by_sensor = defaultdict(list)                  # defaultdict evita comprobar si la clave existe
    for m in read_measurements(path):
        by_sensor[(m["device"], m["sensor"])].append(m["value"])
    for (dev, sensor), vals in sorted(by_sensor.items()):
        print(f"{dev:10s} {sensor:12s} n={len(vals):2d} min={min(vals):7.2f} max={max(vals):7.2f} prom={sum(vals)/len(vals):7.2f}")
