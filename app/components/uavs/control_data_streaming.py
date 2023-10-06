import schedule

from app.lib.broadcaster import send_notification
from app.components.uavs.get_uav_data import get_uav_data

last_location = {
    'lat': 51.505,
    'lon': -0.09,
}

def _send_data_of(uav):
    # data = get_uav_data(uav)

    last_location['lat'] += 0.001
    last_location['lon'] += 0.001

    data = {
        'status': {
            'armed': True,
            'in_air': True,
            'state': 1
        },
        'battery': {
            'id': 1,
            'voltage_level': 1.1,
            'power_supply_status': 1.1
        },
        'gps': {
            'lat': last_location['lat'],
            'lon': last_location['lon'],
            'abs': 1.1,
            'satellites_number': 1
        }
    }

    print("sending data of:", uav)

    send_notification(uav, "data_updated", data)

    print("sent")


_streaming_jobs = {}


def start_data_streaming(uavs):
    print(f'Requested UAVs: {uavs}')
    for uav in uavs:
        job = schedule.every(1).seconds.do(lambda: _send_data_of(uav))

        _streaming_jobs[uav] = job


def stop_data_streaming(uavs):
    for uav in uavs:
        if _streaming_jobs[uav] is not None:
            schedule.cancel_job(_streaming_jobs[uav])
