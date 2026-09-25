#!/usr/bin/env python3
"""
02_sensor_statistics.py
Programa 2: estadisticas de un sensor (con dataclass) + serie temporal basica:
promedio, mediana, desviacion, min, max, media movil y deteccion de picos con z-score.

Ejecutar: python 02_sensor_statistics.py    (solo libreria estandar)
"""
from dataclasses import dataclass
from statistics import mean, median, pstdev
from collections import deque


@dataclass(frozen=True)          # frozen: inmutable, seguro para compartir entre partes del programa
class Stats:
    n: int
    mean: float
    median: float
    stdev: float
    min: float
    max: float


def compute_stats(values):
    """Devuelve Stats o None si no hay datos (evita division entre cero)."""
    values = list(values)
    if not values:
        return None
    return Stats(len(values), mean(values), median(values), pstdev(values), min(values), max(values))


def moving_average(values, window=3):
    """Media movil con deque de tamano fijo (memoria O(window))."""
    buf, out = deque(maxlen=window), []
    for v in values:
        buf.append(v)
        out.append(sum(buf) / len(buf))      # al inicio usa las muestras disponibles
    return out


def zscore_outliers(values, threshold=2.0):
    """Marca indices cuyo |z| supera el umbral. Con pocos datos el z-score es poco robusto."""
    s = compute_stats(values)
    if s is None or s.stdev == 0:
        return []
    return [i for i, v in enumerate(values) if abs(v - s.mean) / s.stdev > threshold]


if __name__ == "__main__":
    temps = [78.0, 79.5, 80.1, 79.8, 80.4, 95.0, 80.0, 79.7]
    print(compute_stats(temps))
    print("media movil(3):", [round(x, 2) for x in moving_average(temps)])
    print("picos (indices):", zscore_outliers(temps))

# Salida esperada:
# Stats(n=8, mean=81.5625, median=79.9, stdev=5.12370410445412, min=78.0, max=95.0)
# media movil(3): [78.0, 78.75, 79.2, 79.8, 80.1, 85.07, 85.13, 84.9]
# picos (indices): [5]
