import os
from typing import TypedDict


class _Env(TypedDict):
    MONGODB_URI: str
    MQTT_BROKER: str
    MQTT_BROKER_PORT: int


class _Config(TypedDict):
    env: _Env


if os.environ["MONGODB_URI"] is None:
    raise Exception("MISSING_ENV_VARIABLES", "should set MONGODB_URI in the env")

if os.environ["MQTT_BROKER"] is None:
    raise Exception("MISSING_ENV_VARIABLES", "should set MQTT_BROKER in the env")

if os.environ["MQTT_BROKER_PORT"] is None:
    raise Exception("MISSING_ENV_VARIABLES", "should set MQTT_BROKER_PORT in the env")

app_config: _Config = {
    "env": {
        "MONGODB_URI": os.environ["MONGODB_URI"],
        "MQTT_BROKER": os.environ["MQTT_BROKER"],
        "MQTT_BROKER_PORT": int(os.environ["MQTT_BROKER_PORT"]),
    }
}
