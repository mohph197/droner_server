from app.lib.mongodb import mongodb
from app.lib.broadcaster import send_notification
import schedule


def check_battery_stats(uav):
    last_doc = list(
        mongodb["bat"].find({"uav": uav, "type": "vl"}).sort("timestamp", -1).limit(1)
    )[0]

    voltage_level = float(last_doc["data"])

    if voltage_level < 5.0:
        send_notification(uav, "battery_low", voltage_level)


def start_battery_check():
    uavs = mongodb["bat"].distinct("uav")

    for uav in uavs:
        schedule.every(1).seconds.do(lambda: check_battery_stats(uav))
