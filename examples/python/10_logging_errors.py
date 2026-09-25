#!/usr/bin/env python3
"""
10_logging_errors.py
Programa 10: registrar errores con `logging` (en lugar de print) y ROTAR archivos.

Por que logging: niveles (DEBUG/INFO/WARNING/ERROR/CRITICAL), timestamps, destino configurable
(consola + archivo), y rotacion para que un servicio de larga duracion no llene el disco.

Ejecutar: python 10_logging_errors.py      -> escribe ./gateway.log (se rota a 200 kB x 3 archivos)
"""
import logging
from logging.handlers import RotatingFileHandler


def setup_logging(path="gateway.log"):
    log = logging.getLogger("gateway")
    log.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s %(levelname)-8s %(name)s: %(message)s")
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)                          # consola: solo INFO o mayor
    console.setFormatter(fmt)
    fileh = RotatingFileHandler(path, maxBytes=200_000, backupCount=3, encoding="utf-8")
    fileh.setLevel(logging.DEBUG)                           # archivo: todo el detalle
    fileh.setFormatter(fmt)
    if not log.handlers:                                    # evita handlers duplicados si se llama 2 veces
        log.addHandler(console)
        log.addHandler(fileh)
    return log


def read_sensor(log, raw):
    try:
        value = float(raw)
        log.debug("lectura cruda=%r", raw)                  # %r con argumentos: no formatea si el nivel esta desactivado
        if value < -40 or value > 150:
            log.warning("valor fuera de rango: %.1f", value)
        return value
    except ValueError:
        log.exception("no se pudo convertir %r", raw)       # exception() incluye el traceback
        return None


if __name__ == "__main__":
    log = setup_logging()
    log.info("gateway iniciado")
    for r in ["80.2", "abc", "400"]:
        read_sensor(log, r)
    log.error("broker inaccesible; se activa el buffer local")

# Salida en consola (INFO+):
# ... INFO     gateway: gateway iniciado
# ... ERROR    gateway: no se pudo convertir 'abc'
# Traceback (most recent call last): ...   (por log.exception)
# ... WARNING  gateway: valor fuera de rango: 400.0
# ... ERROR    gateway: broker inaccesible; se activa el buffer local
