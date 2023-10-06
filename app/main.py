import os
from dotenv import load_dotenv

load_dotenv()

from app.web.fastapi.main import start_fastapi_webserver
from app.components.real_time_data_capture.mqtt_events_capture import (
    start_real_time_data_capture,
)


start_real_time_data_capture()

app = start_fastapi_webserver()
