# MQTT Health Monitor Setup

## Install Required Package

```bash
pip install paho-mqtt
```

---

## Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Start MQTT Listener

```bash
python manage.py mqtt_listener
```

Expected Output:

```bash
Connected with code 0
```

---

## Run Django Server

Open another terminal and run:

```bash
python manage.py runserver
```

Server URL:

```bash
http://127.0.0.1:8000/
```

---

## Optional: Publish Test MQTT Data

```python
import paho.mqtt.client as mqtt
import json

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883, 60)

data = {
    "heart_rate": 82,
    "spo2": 97,
    "glucose": 120,
    "level": "Normal",
    "bp_sys": 120,
    "bp_dia": 80,
    "bp_pulse": 72
}

client.publish("health/healthMonitor", json.dumps(data))
client.disconnect()
```

---

## MQTT Topic

```bash
health/healthMonitor
```

---

## Project Structure

```bash
your_app/
│
├── management/
│   ├── __init__.py
│   └── commands/
│       ├── __init__.py
│       └── mqtt_listener.py
```
