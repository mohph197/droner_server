import schedule

from app.lib.broadcaster import send_notification
from app.components.uavs.get_uav_data import get_uav_data

last_location = {
    "uav1": {
        "lat": 51.505,
        "lon": -0.09,
    },
    "uav2": {
        "lat": 51.505,
        "lon": -0.09,
    },
}


def _send_data_of(uav):
    # data = get_uav_data(uav)

    last_location[uav]["lat"] += 0.002 if uav == "uav1" else -0.001
    last_location[uav]["lon"] += 0.002 if uav == "uav2" else -0.001

    data = {
        "status": {"armed": True, "in_air": True, "state": 1},
        "battery": {"id": 1, "voltage_level": 1.1, "power_supply_status": 1.1},
        "gps": {
            "lat": last_location[uav]["lat"],
            "lon": last_location[uav]["lon"],
            "abs": 1.1,
            "satellites_number": 1,
        },
    }

    print("sending data of:", uav)
    print(data["gps"])

    send_notification(uav, "data_updated", data)

    print("sent")


def _send_data_of_uavs():
    for uav in _uavs_active:
        _send_data_of(uav)


_uavs_active = []
_streaming_job = []


def start_data_streaming(uavs):
    print(f"Requested UAVs: {uavs}")

    for uav in uavs:
        if uav in _uavs_active:
            continue
        else:
            _uavs_active.append(uav)

    if len(_streaming_job) == 0:
        job = schedule.every(1).seconds.do(_send_data_of_uavs)

        _streaming_job.append(job)


def stop_data_streaming(uavs):
    for uav in uavs:
        if uav in _uavs_active:
            _uavs_active.remove(uav)

    if len(_streaming_job) != 0:
        for job in _streaming_job:
            if job is not None:
                schedule.cancel_job(job)
                _streaming_job.remove(job)
