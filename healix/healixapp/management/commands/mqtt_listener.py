from django.core.management.base import BaseCommand
import paho.mqtt.client as mqtt
import json
from django.core.cache import cache
class Command(BaseCommand):
    help = "MQTT listener"

    def handle(self, *args, **kwargs):
        import paho.mqtt.client as mqtt
        import json

        def on_connect(client, userdata, flags, rc):
            print("Connected with code", rc)
            client.subscribe("health/healthMonitor")

        def on_message(client, userdata, msg):
            try:
                data = json.loads(msg.payload.decode())

                cache.set("latest_vitals", {
                    "heart_rate": data.get("heart_rate"),
                    "spo2": data.get("spo2"),
                    "glucose": data.get("glucose"),
                    "level": data.get("level"),
                    "bp_sys": data.get("bp_sys"),
                    "bp_dia": data.get("bp_dia"),
                    "bp_pulse": data.get("bp_pulse"),
                }, timeout=60)

                print("Cached:", data)

            except Exception as e:
                print("MQTT ERROR:", e)

        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect("broker.hivemq.com", 1883, 60)
        client.loop_forever()
