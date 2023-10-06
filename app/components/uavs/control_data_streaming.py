import schedule

from app.lib.broadcaster import send_notification
from app.components.uavs.get_uav_data import get_uav_data


def _send_data_of(uav):
    data = get_uav_data(uav)

    print("sending", data)

    send_notification(uav, "data_updated", data)

    print("sent")


_streaming_jobs = {}


def start_data_streaming(uavs):
    for uav in uavs:
        job = schedule.every(1).seconds.do(lambda: _send_data_of(uav))

        _streaming_jobs[uav] = job


def stop_data_streaming(uavs):
    for uav in uavs:
        if _streaming_jobs[uav] is not None:
            schedule.cancel_job(_streaming_jobs[uav])
