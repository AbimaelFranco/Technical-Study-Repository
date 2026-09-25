#!/usr/bin/env python3
"""
mock_api_server.py
API REST minima para probar los clientes de telemetria SIN instalar nada (solo libreria estandar).
NO es un servidor de produccion: sin autenticacion, sin TLS, sin persistencia real.

Endpoints:
  POST /api/v1/measurements   cuerpo JSON (un objeto o una lista) -> 201 {"accepted":n,"duplicates":m}
  GET  /api/v1/measurements   -> ultimas mediciones guardadas
  GET  /health                -> 200 {"status":"ok"}

Idempotencia: la clave (device_id, seq) identifica una medicion; reenviar la misma NO crea un duplicado.
Ejecutar: python mock_api_server.py [--port 8000] [--fail-first N]
   --fail-first N: responde 503 a las primeras N peticiones POST (para probar reintentos).
"""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

STORE = {}            # (device_id, seq) -> medicion
STATE = {"fail_left": 0}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, {"status": "ok"})
        if self.path == "/api/v1/measurements":
            return self._send(200, list(STORE.values())[-50:])
        self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/v1/measurements":
            return self._send(404, {"error": "not found"})
        if STATE["fail_left"] > 0:                          # simula caida del servidor
            STATE["fail_left"] -= 1
            return self._send(503, {"error": "temporarily unavailable"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            return self._send(400, {"error": "invalid json"})
        items = payload if isinstance(payload, list) else [payload]
        accepted = duplicates = 0
        for it in items:
            try:
                key = (it["device_id"], int(it["seq"]))
            except (KeyError, TypeError, ValueError):
                return self._send(422, {"error": "device_id and seq are required"})
            if key in STORE:
                duplicates += 1
            else:
                STORE[key] = it
                accepted += 1
        self._send(201, {"accepted": accepted, "duplicates": duplicates})

    def log_message(self, fmt, *args):           # silencia el log por peticion
        pass


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--fail-first", type=int, default=0)
    a = ap.parse_args()
    STATE["fail_left"] = a.fail_first
    print(f"escuchando en http://127.0.0.1:{a.port}  (Ctrl+C para salir)")
    ThreadingHTTPServer(("127.0.0.1", a.port), Handler).serve_forever()
