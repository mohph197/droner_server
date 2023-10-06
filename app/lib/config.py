import os
from typing import TypedDict

from dotenv import load_dotenv


load_dotenv()


class _Env(TypedDict):
    MONGODB_URI: str
    MQTT_BROKER: str
    MQTT_BROKER_PORT: int
    PUSHER_APP_ID: str
    PUSHER_APP_KEY: str
    PUSHER_APP_SECRET: str


class _Config(TypedDict):
    env: _Env


if os.environ["MONGODB_URI"] is None:
    raise Exception("MISSING_ENV_VARIABLES", "should set MONGODB_URI in the env")

if os.environ["MQTT_BROKER"] is None:
    raise Exception("MISSING_ENV_VARIABLES", "should set MQTT_BROKER in the env")

if os.environ["MQTT_BROKER_PORT"] is None:
    raise Exception("MISSING_ENV_VARIABLES", "should set MQTT_BROKER_PORT in the env")

if os.environ["PUSHER_APP_ID"] is None:
    raise Exception("MISSING_ENV_VARIABLES", "should set PUSHER_APP_ID in the env")

if os.environ["PUSHER_APP_KEY"] is None:
    raise Exception("MISSING_ENV_VARIABLES", "should set PUSHER_APP_KEY in the env")

if os.environ["PUSHER_APP_SECRET"] is None:
    raise Exception("MISSING_ENV_VARIABLES", "should set PUSHER_APP_SECRET in the env")

app_config: _Config = {
    "env": {
        "MONGODB_URI": os.environ["MONGODB_URI"],
        "MQTT_BROKER": os.environ["MQTT_BROKER"],
        "MQTT_BROKER_PORT": int(os.environ["MQTT_BROKER_PORT"]),
        "PUSHER_APP_ID": os.environ["PUSHER_APP_ID"],
        "PUSHER_APP_KEY": os.environ["PUSHER_APP_KEY"],
        "PUSHER_APP_SECRET": os.environ["PUSHER_APP_SECRET"],
    }
}
