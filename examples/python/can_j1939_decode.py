#!/usr/bin/env python3
"""
can_j1939_decode.py
Decodifica el ID de 29 bits de J1939 y dos mensajes de ejemplo. Solo libreria estandar.

Estructura del ID (29 bits):   P(3) | R(1) | DP(1) | PF(8) | PS(8) | SA(8)
  - Prioridad P: 0 = maxima prioridad ... 7 = minima.
  - PGN (Parameter Group Number) se forma con [R, DP, PF, PS]:
        si PF >= 240 (PDU2, difusion):  PGN = R DP PF PS      (PS es extension del grupo)
        si PF <  240 (PDU1, punto a punto): PGN = R DP PF 00  (PS es la direccion de DESTINO)
  - SA: direccion de origen (source address).

Ejemplos usados (SPN/PGN de uso comun; VERIFICA en SAE J1939-71 o en el DBC del fabricante):
  PGN 61444 (0xF004) EEC1: SPN 190 engine speed, bytes 4-5 (indices 3-4), 0.125 rpm/bit
  PGN 65262 (0xFEEE) ET1 : SPN 110 engine coolant temperature, byte 1, 1 C/bit, offset -40 C
  Valor 0xFF / 0xFFFF = "no disponible".

En Linux con SocketCAN se obtendrian tramas con `python-can` (pip install python-can);
aqui se usan tuplas (id, datos) para poder ejecutar sin hardware.
Ejecutar: python can_j1939_decode.py
"""


def split_j1939_id(can_id: int):
    priority = (can_id >> 26) & 0x7
    dp = (can_id >> 24) & 0x1
    r = (can_id >> 25) & 0x1
    pf = (can_id >> 16) & 0xFF
    ps = (can_id >> 8) & 0xFF
    sa = can_id & 0xFF
    if pf >= 240:                                  # PDU2: PS forma parte del PGN
        pgn = (r << 17) | (dp << 16) | (pf << 8) | ps
        dest = None                                # difusion
    else:                                          # PDU1: PS es el destino
        pgn = (r << 17) | (dp << 16) | (pf << 8)
        dest = ps
    return {"priority": priority, "pgn": pgn, "dest": dest, "sa": sa}


def decode(can_id: int, data: bytes):
    h = split_j1939_id(can_id)
    out = dict(h)
    if h["pgn"] == 61444 and len(data) >= 5:                       # EEC1
        raw = data[3] | (data[4] << 8)                              # little-endian
        out["engine_speed_rpm"] = None if raw >= 0xFF00 else raw * 0.125
    elif h["pgn"] == 65262 and len(data) >= 1:                     # ET1
        out["coolant_temp_c"] = None if data[0] == 0xFF else data[0] - 40
    return out


if __name__ == "__main__":
    frames = [
        (0x0CF00400, bytes([0xFF, 0xFF, 0xFF, 0xD0, 0x39, 0xFF, 0xFF, 0xFF])),   # 1850 rpm
        (0x18FEEE00, bytes([0x7D, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])),   # 85 C
        (0x18FEEE00, bytes([0xFF] * 8)),                                          # no disponible
    ]
    for cid, data in frames:
        print(f"0x{cid:08X} -> {decode(cid, data)}")

# Salida esperada:
# 0x0CF00400 -> {'priority': 3, 'pgn': 61444, 'dest': None, 'sa': 0, 'engine_speed_rpm': 1850.0}
# 0x18FEEE00 -> {'priority': 6, 'pgn': 65262, 'dest': None, 'sa': 0, 'coolant_temp_c': 85}
# 0x18FEEE00 -> {'priority': 6, 'pgn': 65262, 'dest': None, 'sa': 0, 'coolant_temp_c': None}
