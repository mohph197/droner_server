import pusher
from app.lib.config import app_config

_pusher_client = pusher.Pusher(
    app_id=app_config["env"]["PUSHER_APP_ID"],
    key=app_config["env"]["PUSHER_APP_KEY"],
    secret=app_config["env"]["PUSHER_APP_SECRET"],
    cluster="eu",
    ssl=True,
)


def send_notification(topic, event, data):
    _pusher_client.trigger(topic, event, data)
