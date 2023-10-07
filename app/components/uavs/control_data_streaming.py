import schedule

from app.lib.broadcaster import send_notification
from app.components.uavs.get_uav_data import get_uav_data


def _send_data_of(uav):
    data = get_uav_data(uav)

    print("sending", data)
    send_notification(uav, "data_updated", data)
    print("sent")


def _send_data_of_uavs():
    for uav in _uavs_active:
        _send_data_of(uav)


_uavs_active = []
_streaming_job = []


def start_data_streaming(uavs):
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
