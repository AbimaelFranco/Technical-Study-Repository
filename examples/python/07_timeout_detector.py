#!/usr/bin/env python3
"""
07_timeout_detector.py
Programa 7: detectar perdida de comunicacion por timeout (watchdog de datos / heartbeat).

Idea: cada dispositivo debe "hablar" al menos cada `timeout_s`. Si no, se declara OFFLINE
y cuando vuelve a hablar, ONLINE. Usa time.monotonic() (no salta si cambia la hora del sistema).

Ejecutar: python 07_timeout_detector.py     (libreria estandar; simula el tiempo)
"""
import time


class LinkMonitor:
    def __init__(self, timeout_s, clock=time.monotonic):
        self.timeout_s = timeout_s
        self.clock = clock                 # inyectable: permite probar sin esperar
        self.last_seen = {}                # device_id -> instante del ultimo dato
        self.online = {}                   # device_id -> bool

    def heard_from(self, dev):
        """Llamar en cada mensaje/heartbeat recibido. Devuelve un evento si cambio el estado."""
        self.last_seen[dev] = self.clock()
        if not self.online.get(dev, False):
            self.online[dev] = True
            return f"{dev}: ONLINE"
        return None

    def check(self):
        """Llamar periodicamente. Devuelve la lista de eventos OFFLINE nuevos."""
        now, events = self.clock(), []
        for dev, t in self.last_seen.items():
            if self.online[dev] and now - t > self.timeout_s:
                self.online[dev] = False
                events.append(f"{dev}: OFFLINE (silencio {now - t:.1f} s > {self.timeout_s} s)")
        return events


if __name__ == "__main__":
    fake_now = [0.0]                                  # reloj simulado
    mon = LinkMonitor(timeout_s=5.0, clock=lambda: fake_now[0])
    schedule = {0: "tractor01", 2: "tractor01", 3: "bomba02"}   # segundo -> quien habla
    for t in range(0, 16):
        fake_now[0] = float(t)
        if t in schedule and (ev := mon.heard_from(schedule[t])):
            print(f"t={t:2d}s {ev}")
        for ev in mon.check():
            print(f"t={t:2d}s {ev}")
        if t == 12:
            print(f"t={t:2d}s (tractor01 vuelve)"); ev = mon.heard_from("tractor01"); print(f"t={t:2d}s {ev}")

# Salida esperada:
# t= 0s tractor01: ONLINE
# t= 3s bomba02: ONLINE
# t= 8s tractor01: OFFLINE (silencio 6.0 s > 5.0 s)
# t= 9s bomba02: OFFLINE (silencio 6.0 s > 5.0 s)
# t=12s (tractor01 vuelve)
# t=12s tractor01: ONLINE
# (se declara OFFLINE cuando el silencio SUPERA el timeout; aqui se comprueba cada segundo)
