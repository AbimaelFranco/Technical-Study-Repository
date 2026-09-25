#!/usr/bin/env python3
"""
mqtt_publisher.py
Publica telemetria por MQTT con paho-mqtt (pip install paho-mqtt). REQUIERE un broker (p. ej. Mosquitto).
NO se ejecuto contra un broker dentro de este repositorio: es una plantilla didactica.

Probar localmente (Linux):
    sudo apt install mosquitto mosquitto-clients
    mosquitto_sub -h localhost -t 'ingenio/+/+/telemetry' -v          # terminal 1
    python mqtt_publisher.py                                          # terminal 2

Ideas clave (MQTT 3.1.1 / 5.0, OASIS):
  - Topic jerarquico:  ingenio/<sitio>/<maquina>/telemetry
  - QoS 1 = "al menos una vez": puede haber DUPLICADOS -> el consumidor debe ser idempotente (device_id + seq).
  - LWT (Last Will and Testament): el broker publica "offline" si el cliente se cae sin desconectar.
  - retain=True en el estado: un suscriptor nuevo recibe de inmediato el ultimo estado conocido.
  - Puerto 1883 sin cifrar; 8883 con TLS. En produccion: TLS + usuario/contrasena o certificados + ACL.
API de paho-mqtt 2.x (Client(CallbackAPIVersion.VERSION2)); en 1.x cambia la firma de los callbacks.
"""
import json
import time

import paho.mqtt.client as mqtt

BROKER, PORT = "localhost", 1883
DEVICE = "tractor01"
TOPIC_T = f"ingenio/costa-sur/{DEVICE}/telemetry"
TOPIC_S = f"ingenio/costa-sur/{DEVICE}/status"


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"gw-{DEVICE}")
    # client.tls_set()                       # en produccion (con CA/certificados) y puerto 8883
    # client.username_pw_set("usuario", "clave")
    client.will_set(TOPIC_S, json.dumps({"state": "offline"}), qos=1, retain=True)   # LWT
    client.connect(BROKER, PORT, keepalive=30)
    client.loop_start()                       # hilo de red en segundo plano (reconexion automatica)
    client.publish(TOPIC_S, json.dumps({"state": "online"}), qos=1, retain=True)

    for seq in range(1, 6):
        msg = {"device_id": DEVICE, "seq": seq, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "sensor": "temp_motor", "value": 80.0 + seq / 10, "unit": "C", "quality": "good"}
        info = client.publish(TOPIC_T, json.dumps(msg), qos=1)
        info.wait_for_publish(timeout=5)      # espera el PUBACK; si vence, encolar en buffer local
        print("publicado", msg["seq"], "ok" if info.is_published() else "PENDIENTE")
        time.sleep(1)

    client.publish(TOPIC_S, json.dumps({"state": "offline"}), qos=1, retain=True)
    client.loop_stop()
    client.disconnect()


if __name__ == "__main__":
    main()
