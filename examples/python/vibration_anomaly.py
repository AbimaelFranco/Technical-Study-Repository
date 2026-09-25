#!/usr/bin/env python3
"""
vibration_anomaly.py
CASO B (docs/14): adquisicion de vibracion y deteccion de anomalias, solo libreria estandar.

Se genera una senal sintetica de un rodamiento: 50 Hz (rotacion) + ruido, y luego una falla
que agrega un componente de alta frecuencia (3 kHz) y aumenta la amplitud.
Indicadores calculados por ventana:
  - RMS  : energia general de la vibracion.
  - Pico y factor de cresta (pico/RMS): sube cuando hay impactos (tipico de defectos tempranos).
  - Energia por bandas via DFT simple (didactico; en produccion se usa FFT con numpy/scipy).
Deteccion: se aprende una LINEA BASE en una ventana sana y se marca anomalia si RMS > baseline * factor.

Muestreo: fs = 10 kHz -> Nyquist = 5 kHz. Un componente de 3 kHz se ve; uno de 7 kHz produciria ALIASING.
Ejecutar: python vibration_anomaly.py
"""
import math
import random

FS = 10_000            # frecuencia de muestreo en Hz
N = 1000               # muestras por ventana (0.1 s)
random.seed(1)         # reproducible


def make_window(fail=False):
    out = []
    for n in range(N):
        t = n / FS
        x = 1.0 * math.sin(2 * math.pi * 50 * t) + random.gauss(0, 0.1)
        if fail:
            x = 1.6 * math.sin(2 * math.pi * 50 * t) + 0.8 * math.sin(2 * math.pi * 3000 * t) + random.gauss(0, 0.2)
        out.append(x)
    return out


def rms(x):
    return math.sqrt(sum(v * v for v in x) / len(x))


def band_energy(x, f_lo, f_hi, step=50):
    """Energia aproximada en [f_lo, f_hi] Hz evaluando la DFT solo en frecuencias elegidas (costo O(N*K))."""
    total = 0.0
    for f in range(f_lo, f_hi + 1, step):
        re = sum(v * math.cos(2 * math.pi * f * n / FS) for n, v in enumerate(x))
        im = sum(v * math.sin(2 * math.pi * f * n / FS) for n, v in enumerate(x))
        total += (re * re + im * im) / (N * N)
    return total


def indicators(x):
    r = rms(x)
    peak = max(abs(v) for v in x)
    return {"rms": r, "peak": peak, "crest": peak / r,
            "low_band(0-100Hz)": band_energy(x, 0, 100), "high_band(2-4kHz)": band_energy(x, 2000, 4000, step=250)}


if __name__ == "__main__":
    baseline = indicators(make_window())
    print("linea base:", {k: round(v, 3) for k, v in baseline.items()})
    for label, fail in [("sano", False), ("sano", False), ("FALLA", True)]:
        ind = indicators(make_window(fail))
        anomaly = ind["rms"] > 1.5 * baseline["rms"] or ind["high_band(2-4kHz)"] > 10 * max(baseline["high_band(2-4kHz)"], 1e-6)
        print(f"{label:6s} rms={ind['rms']:.2f} crest={ind['crest']:.2f} alta_freq={ind['high_band(2-4kHz)']:.4f} -> "
              f"{'ANOMALIA' if anomaly else 'normal'}")

# Salida esperada (numeros verificados con random.seed(1)):
# linea base: {'rms': 0.719, 'peak': 1.235, 'crest': 1.717, 'low_band(0-100Hz)': 0.254, 'high_band(2-4kHz)': 0.0}
# sano   rms=0.71 crest=1.75 alta_freq=0.0001 -> normal
# sano   rms=0.70 crest=1.85 alta_freq=0.0001 -> normal
# FALLA  rms=1.29 crest=2.13 alta_freq=0.1560 -> ANOMALIA
