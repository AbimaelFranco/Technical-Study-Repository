#!/usr/bin/env python3
"""
01_filter_out_of_range.py
Programa 1 del modulo 04: filtrar lecturas fuera de rango.

Que hace: separa una lista de lecturas en "validas" y "rechazadas" (con el motivo).
Por que asi: no se descartan datos en silencio; se conserva el motivo para diagnostico.

Ejecutar:  python 01_filter_out_of_range.py     (solo libreria estandar, Python >= 3.9)
"""
import math

# Rango fisicamente plausible para la temperatura de un motor (ejemplo didactico).
TEMP_MIN, TEMP_MAX = -40.0, 150.0
SENTINELS = {-127.0: "sensor desconectado (DS18B20)"}  # valores "magicos" conocidos de drivers


def classify_reading(value):
    """Devuelve (es_valida, motivo). Entrada: cualquier objeto; salida: tupla."""
    if value is None:
        return False, "sin dato"
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False, f"tipo invalido: {type(value).__name__}"
    if math.isnan(value) or math.isinf(value):
        return False, "NaN/inf"
    if value in SENTINELS:
        return False, SENTINELS[value]
    if not (TEMP_MIN <= value <= TEMP_MAX):
        return False, f"fuera de rango [{TEMP_MIN}, {TEMP_MAX}]"
    return True, "ok"


def filter_readings(readings):
    valid, rejected = [], []
    for r in readings:                       # O(n): una pasada
        ok, reason = classify_reading(r)
        (valid if ok else rejected).append(r if ok else (r, reason))
    return valid, rejected


if __name__ == "__main__":
    data = [78.5, 80.1, -127.0, 96.3, None, "abc", float("nan"), 200.0, 85.0]
    valid, rejected = filter_readings(data)
    print("validas   :", valid)
    print("rechazadas:")
    for item, why in rejected:
        print(f"   {item!r:>8} -> {why}")

# Salida esperada:
# validas   : [78.5, 80.1, 96.3, 85.0]
# rechazadas:
#   -127.0 -> sensor desconectado (DS18B20)
#     None -> sin dato
#    'abc' -> tipo invalido: str
#      nan -> NaN/inf
#    200.0 -> fuera de rango [-40.0, 150.0]
