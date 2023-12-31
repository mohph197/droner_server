import schedule
from threading import Thread

from app.components.uavs.missions.init_missions_scheduler import (
    start_missions_statuses_check,
)


from app.web.fastapi.main import start_fastapi_webserver

from app.components.uavs.battery_check import start_battery_check

from app.components.real_time_data_capture.mqtt_events_capture import (
    start_real_time_data_capture,
)
from app.components.uavs.fake_uavs_data_filler import (
    start_fake_uavs_data_filling,
)

start_real_time_data_capture()

start_fake_uavs_data_filling()
start_battery_check()
start_missions_statuses_check()


def setup_schduler():
    while True:
        schedule.run_pending()


schedule_thread = Thread(target=setup_schduler)
schedule_thread.start()


app = start_fastapi_webserver()
