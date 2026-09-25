#!/usr/bin/env python3
"""
09_alerts_thresholds.py
Programa 9: generar alertas con umbrales, con HISTERESIS y confirmacion por N muestras.

Problemas que resuelve:
  - Una sola lectura alta (ruido) NO debe disparar una alarma: se exigen `confirm` muestras seguidas.
  - Una temperatura que oscila alrededor del umbral no debe generar "alarma/normal/alarma/...":
    la alarma se limpia solo cuando baja de (umbral - histeresis).

Ejecutar: python 09_alerts_thresholds.py   (libreria estandar)
"""
from dataclasses import dataclass


@dataclass
class ThresholdAlert:
    name: str
    high: float            # umbral de alarma
    hysteresis: float      # banda de retorno
    confirm: int = 3       # muestras consecutivas necesarias
    active: bool = False
    _count: int = 0

    def update(self, value):
        """Devuelve 'RAISE', 'CLEAR' o None."""
        if not self.active:
            self._count = self._count + 1 if value >= self.high else 0
            if self._count >= self.confirm:
                self.active, self._count = True, 0
                return "RAISE"
        else:
            if value < self.high - self.hysteresis:
                self.active = False
                return "CLEAR"
        return None


if __name__ == "__main__":
    alert = ThresholdAlert("temp_motor_alta", high=95.0, hysteresis=3.0, confirm=3)
    series = [90, 96, 90, 96, 97, 98, 99, 94, 93, 91.9, 90]
    for i, v in enumerate(series):
        ev = alert.update(v)
        if ev:
            print(f"muestra {i:2d} valor={v:5.1f} -> {ev} {alert.name}")

# Salida esperada:
# muestra  5 valor= 98.0 -> RAISE temp_motor_alta   (96, 97, 98: tres muestras seguidas >= 95)
# muestra  9 valor= 91.9 -> CLEAR temp_motor_alta   (< 95 - 3 = 92)
