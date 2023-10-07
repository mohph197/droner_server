from app.components.uavs.missions.models.point import Point

from .fake_uavs_data_filler import fake_data


def goto(target_uav: str, destination: Point, speed: int):
    if target_uav not in fake_data.keys():
        return

    fake_data[target_uav]["in_air"]["value"] = True
    fake_data[target_uav]["bat"]["gps"]["lat"]["next_value_diff"] = (
        destination.lat - fake_data[target_uav]["bat"]["gps"]["lat"]["value"]
    ) / (speed * 10)
    fake_data[target_uav]["bat"]["gps"]["lon"]["next_value_diff"] = (
        destination.lon - fake_data[target_uav]["bat"]["gps"]["lon"]["value"]
    ) / (speed * 10)


def land(target_uav: str):
    if target_uav not in fake_data.keys():
        return

    fake_data[target_uav]["in_air"]["value"] = False
    fake_data[target_uav]["bat"]["vl"]["next_value_diff"] = 0
    fake_data[target_uav]["bat"]["gps"]["lat"]["next_value_diff"] = 0
    fake_data[target_uav]["bat"]["gps"]["lon"]["next_value_diff"] = 0
