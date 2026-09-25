#!/usr/bin/env python3
"""
04_parse_json.py
Programa 4: parsear y validar mensajes JSON de telemetria.

Mensaje esperado:
  {"device_id":"tractor01","ts":"2026-03-01T06:00:00Z","seq":10,
   "sensor":"temp_motor","value":80.4,"unit":"C","quality":"good"}

Ejecutar: python 04_parse_json.py   (libreria estandar)
"""
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

REQUIRED = {"device_id": str, "ts": str, "seq": int, "sensor": str, "value": (int, float), "unit": str}
QUALITIES = {"good", "uncertain", "bad"}


class InvalidMessage(ValueError):
    """Excepcion propia: distingue mensajes malos de otros errores del programa."""


@dataclass
class Telemetry:
    device_id: str
    ts: datetime
    seq: int
    sensor: str
    value: float
    unit: str
    quality: str = "good"


def parse_message(raw: str) -> Telemetry:
    try:
        obj = json.loads(raw)                            # JSONDecodeError (subclase de ValueError) si esta mal formado
    except json.JSONDecodeError as e:
        raise InvalidMessage(f"JSON invalido: {e}") from e
    if not isinstance(obj, dict):
        raise InvalidMessage("se esperaba un objeto JSON")
    for key, typ in REQUIRED.items():
        if key not in obj:
            raise InvalidMessage(f"falta el campo '{key}'")
        if not isinstance(obj[key], typ) or isinstance(obj[key], bool):
            raise InvalidMessage(f"tipo incorrecto en '{key}'")
    quality = obj.get("quality", "good")                 # campo opcional con valor por defecto
    if quality not in QUALITIES:
        raise InvalidMessage(f"quality desconocida: {quality}")
    try:
        ts = datetime.fromisoformat(obj["ts"].replace("Z", "+00:00"))   # 'Z' = UTC
    except ValueError as e:
        raise InvalidMessage(f"timestamp invalido: {e}") from e
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)             # regla: sin zona = UTC
    return Telemetry(obj["device_id"], ts, obj["seq"], obj["sensor"], float(obj["value"]), obj["unit"], quality)


if __name__ == "__main__":
    samples = [
        '{"device_id":"tractor01","ts":"2026-03-01T06:00:00Z","seq":10,"sensor":"temp_motor","value":80.4,"unit":"C"}',
        '{"device_id":"tractor01","seq":11}',
        'not json',
        '{"device_id":"t","ts":"ayer","seq":1,"sensor":"x","value":1,"unit":"C"}',
    ]
    for s in samples:
        try:
            t = parse_message(s)
            print("OK  ", asdict(t))
        except InvalidMessage as e:
            print("MAL ", e)

# Salida esperada:
# OK   {'device_id': 'tractor01', 'ts': datetime.datetime(2026, 3, 1, 6, 0, tzinfo=datetime.timezone.utc), 'seq': 10, ...}
# MAL  falta el campo 'ts'
# MAL  JSON invalido: Expecting value: line 1 column 1 (char 0)
# MAL  timestamp invalido: Invalid isoformat string: 'ayer'
