import os
from dotenv import load_dotenv
from threading import Thread
import schedule
from time import sleep

load_dotenv()

from app.web.fastapi.main import start_fastapi_webserver
from app.components.uavs.battery_check import start_battery_check
from app.components.real_time_data_capture.mqtt_events_capture import (
    start_real_time_data_capture, stop_real_time_data_capture
)

thread = Thread(target=start_real_time_data_capture)
thread.start()
start_battery_check()

def loop_schedule():
    while True:
        schedule.run_pending()
        sleep(1)

schedule_thread = Thread(target=loop_schedule)
schedule_thread.start()

app = start_fastapi_webserver()

app.on_event("shutdown")(lambda: stop_real_time_data_capture())