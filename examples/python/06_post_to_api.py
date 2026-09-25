#!/usr/bin/env python3
"""
06_post_to_api.py
Programa 6: enviar mediciones a una API REST con `requests`.

Instalacion: pip install requests
Prueba local: en otra terminal  ->  python mock_api_server.py --fail-first 2
              y aqui            ->  python 06_post_to_api.py

Buenas practicas mostradas:
  - timeout SIEMPRE (requests no tiene timeout por defecto: puede colgarse para siempre).
  - reintentos con backoff exponencial + jitter ante errores transitorios (red, 5xx).
  - NO reintentar errores del cliente (4xx): el mensaje esta mal y fallara siempre.
  - idempotencia: cada medicion lleva (device_id, seq) para que un reintento no duplique.
  - HTTPS y credenciales (token) en produccion; aqui HTTP local solo para practicar.
"""
import random
import time

import requests

API = "http://127.0.0.1:8000/api/v1/measurements"


def post_with_retry(payload, url=API, retries=5, base_delay=0.2, timeout=3.0):
    """Devuelve la respuesta JSON o None si se agotaron los reintentos."""
    for attempt in range(retries + 1):
        try:
            r = requests.post(url, json=payload, timeout=timeout)   # json= serializa y pone Content-Type
            if r.status_code < 300:
                return r.json()
            if 400 <= r.status_code < 500:                           # error del cliente: no reintentar
                print(f"rechazado {r.status_code}: {r.text}")
                return None
            print(f"intento {attempt + 1}: servidor respondio {r.status_code}")   # 5xx: transitorio
        except (requests.ConnectionError, requests.Timeout) as e:
            print(f"intento {attempt + 1}: {type(e).__name__}")
        delay = base_delay * (2 ** attempt) * (0.5 + random.random() / 2)    # backoff exponencial con jitter
        time.sleep(delay)
    return None


if __name__ == "__main__":
    m = {"device_id": "tractor01", "seq": 1, "ts": "2026-03-01T06:00:00Z",
         "sensor": "temp_motor", "value": 80.4, "unit": "C", "quality": "good"}
    print("resultado:", post_with_retry(m))
    print("reenvio  :", post_with_retry(m), "<- duplicates=1: idempotente")

# Salida esperada con el servidor iniciado con --fail-first 2:
# intento 1: servidor respondio 503
# intento 2: servidor respondio 503
# resultado: {'accepted': 1, 'duplicates': 0}
# reenvio  : {'accepted': 0, 'duplicates': 1} <- duplicates=1: idempotente
