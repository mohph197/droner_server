from datetime import datetime
import paho.mqtt.client as mqtt
from app.lib.config import app_config
from app.lib.mongodb import mongodb

client = mqtt.Client()


def _on_connect(client, userdata, flags, rc):
    client.subscribe("uav1/bat/id")
    client.subscribe("uav2/bat/id")
    client.subscribe("uav1/bat/vl")
    client.subscribe("uav2/bat/vl")
    client.subscribe("uav1/bat/pt")
    client.subscribe("uav2/bat/pt")
    client.subscribe("uav1/gps/fx")
    client.subscribe("uav2/gps/fx")
    client.subscribe("uav1/gps/ns")
    client.subscribe("uav2/gps/ns")
    client.subscribe("uav1/gps/lat")
    client.subscribe("uav2/gps/lat")
    client.subscribe("uav1/gps/lon")
    client.subscribe("uav2/gps/lon")
    client.subscribe("uav1/gps/abs")
    client.subscribe("uav2/gps/abs")
    client.subscribe("uav1/gps/rel")
    client.subscribe("uav2/gps/rel")
    client.subscribe("uav1/in_air")
    client.subscribe("uav2/in_air")
    client.subscribe("uav1/armed")
    client.subscribe("uav2/armed")
    client.subscribe("uav1/state")
    client.subscribe("uav2/state")
    client.subscribe("uav1/mav_msg")
    client.subscribe("uav2/mav_msg")
    client.subscribe("uav1/health")
    client.subscribe("uav2/health")
    client.subscribe("uav1/fm")
    client.subscribe("uav2/fm")


def _on_message(client, userdata, msg):
    print(msg.topic, " : ", msg.payload.decode())

    topic = msg.topic
    data = msg.payload.decode()

    if data is '{"1":"Hello world","2":"Welcome to the test connection"}':
        return

    chunks = topic.split("/")

    uav = chunks[0]
    collection = chunks[1]
    type = chunks[2] if len(chunks) == 3 else None

    document = {
        "uav": uav,
        "timestamp": datetime.now(),
        "type": type,
        "data": data,
    }

    mongodb[collection].insert_one(document)


def start_real_time_data_capture():
    print("Starting Real Time Data Capture")
    client.on_connect = _on_connect
    client.on_message = _on_message

    client.connect(
        app_config["env"]["MQTT_BROKER"],
        app_config["env"]["MQTT_BROKER_PORT"],
        keepalive=60,
        bind_port=app_config["env"]["MQTT_BROKER_PORT"],
    )

    client.loop_start()


def stop_real_time_data_capture():
    client.loop_stop()
