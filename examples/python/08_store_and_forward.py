#!/usr/bin/env python3
"""
08_store_and_forward.py
Programa 8: guardar datos localmente durante una desconexion y reenviarlos al volver la red.

Patron "store & forward": el productor SIEMPRE escribe primero en una cola persistente (SQLite);
un enviador aparte lee los pendientes en orden y los borra SOLO tras recibir confirmacion.
=> Si se corta la energia o la red, no se pierde nada; si se reenvia, el servidor ignora
   duplicados gracias a (device_id, seq) (ver mock_api_server.py).

Ejecutar: python 08_store_and_forward.py    (libreria estandar; simula el servidor)
"""
import json
import sqlite3


class OutboxQueue:
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path)
        self.db.execute("""CREATE TABLE IF NOT EXISTS outbox (
            id INTEGER PRIMARY KEY AUTOINCREMENT,   -- orden de llegada
            payload TEXT NOT NULL,                   -- JSON de la medicion (incluye device_id, seq, ts original)
            attempts INTEGER NOT NULL DEFAULT 0)""")
        self.db.commit()

    def put(self, msg: dict):
        self.db.execute("INSERT INTO outbox(payload) VALUES (?)", (json.dumps(msg),))   # ? evita inyeccion SQL
        self.db.commit()                                                                  # durable

    def peek(self, limit=100):
        rows = self.db.execute("SELECT id, payload FROM outbox ORDER BY id LIMIT ?", (limit,)).fetchall()
        return [(i, json.loads(p)) for i, p in rows]

    def ack(self, ids):
        self.db.executemany("DELETE FROM outbox WHERE id = ?", [(i,) for i in ids])
        self.db.commit()

    def size(self):
        return self.db.execute("SELECT COUNT(*) FROM outbox").fetchone()[0]


def flush(queue, send_batch):
    """Envia en lotes. `send_batch(list)` devuelve True si el servidor confirmo. Se detiene en el primer fallo."""
    sent = 0
    while True:
        batch = queue.peek(limit=3)
        if not batch:
            return sent
        if not send_batch([m for _, m in batch]):
            return sent                       # sin red: conservar todo, reintentar luego
        queue.ack([i for i, _ in batch])      # confirmar SOLO tras exito
        sent += len(batch)


if __name__ == "__main__":
    q = OutboxQueue()
    network_up = {"v": False}
    server_received = []

    def send_batch(batch):
        if not network_up["v"]:
            return False
        server_received.extend(batch)
        return True

    for seq in range(1, 8):                    # 7 mediciones mientras NO hay red
        q.put({"device_id": "tractor01", "seq": seq, "ts": f"2026-03-01T06:00:{seq:02d}Z", "value": 80 + seq / 10})
    print("pendientes sin red:", q.size(), "| enviados:", flush(q, send_batch))

    network_up["v"] = True                     # vuelve la red
    print("enviados al volver la red:", flush(q, send_batch), "| pendientes:", q.size())
    print("seq recibidos en orden:", [m["seq"] for m in server_received])

# Salida esperada:
# pendientes sin red: 7 | enviados: 0
# enviados al volver la red: 7 | pendientes: 0
# seq recibidos en orden: [1, 2, 3, 4, 5, 6, 7]
