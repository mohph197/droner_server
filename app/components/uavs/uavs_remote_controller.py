from app.components.uavs.missions.models.point import Point

from .fake_uavs_data_filler import fake_data


def goto(target_uav: str, destination: Point, speed: int):
    if target_uav not in fake_data.keys():
        return

    fake_data[target_uav]["in_air"]["value"] = True
    fake_data[target_uav]["bat"]["vl"]["next_value_diff"] = -0.001

    lat = fake_data[target_uav]["gps"]["lat"]["value"]
    lon = fake_data[target_uav]["gps"]["lon"]["value"]

    fake_data[target_uav]["gps"]["lat"]["next_value_diff"] = (
        destination["lat"] - lat
    ) / (speed * 10)

    fake_data[target_uav]["gps"]["lon"]["next_value_diff"] = (
        destination["lon"] - lon
    ) / (speed * 10)


def land(target_uav: str):
    if target_uav not in fake_data.keys():
        return

    fake_data[target_uav]["in_air"]["value"] = False
    fake_data[target_uav]["bat"]["vl"]["next_value_diff"] = 0
    fake_data[target_uav]["gps"]["lat"]["next_value_diff"] = 0
    fake_data[target_uav]["gps"]["lon"]["next_value_diff"] = 0
