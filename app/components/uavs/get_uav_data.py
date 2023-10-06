from app.lib.mongodb import mongodb


def get_uav_data(uav):
    # Status
    status = {}

    last_doc = list(mongodb["armed"].find({"uav": uav}).sort("timestamp", -1).limit(1))[
        0
    ]
    status["armed"] = True if last_doc["data"] == "1" else False

    last_doc = list(
        mongodb["in_air"].find({"uav": uav}).sort("timestamp", -1).limit(1)
    )[0]
    status["in_air"] = True if last_doc["data"] == "True" else False

    last_doc = list(mongodb["state"].find({"uav": uav}).sort("timestamp", -1).limit(1))[
        0
    ]
    status["state"] = int(last_doc["data"])

    # Battery
    battery = {}

    last_doc = list(
        mongodb["bat"].find({"uav": uav, "type": "id"}).sort("timestamp", -1).limit(1)
    )[0]
    battery["id"] = int(last_doc["data"])

    last_doc = list(
        mongodb["bat"].find({"uav": uav, "type": "vl"}).sort("timestamp", -1).limit(1)
    )[0]
    battery["voltage_level"] = float(last_doc["data"])

    last_doc = list(
        mongodb["bat"].find({"uav": uav, "type": "pt"}).sort("timestamp", -1).limit(1)
    )[0]
    battery["power_supply_status"] = float(last_doc["data"])

    # GPS
    gps = {}

    last_doc = list(
        mongodb["gps"].find({"uav": uav, "type": "lat"}).sort("timestamp", -1).limit(1)
    )[0]
    gps["lat"] = float(last_doc["data"])

    last_doc = list(
        mongodb["gps"].find({"uav": uav, "type": "lon"}).sort("timestamp", -1).limit(1)
    )[0]
    gps["lon"] = float(last_doc["data"])

    last_doc = list(
        mongodb["gps"].find({"uav": uav, "type": "abs"}).sort("timestamp", -1).limit(1)
    )[0]
    gps["abs"] = float(last_doc["data"])

    last_doc = list(
        mongodb["gps"].find({"uav": uav, "type": "ns"}).sort("timestamp", -1).limit(1)
    )[0]
    gps["satellites_number"] = int(last_doc["data"])

    last_doc = list(
        mongodb["gps"].find({"uav": uav, "type": "fx"}).sort("timestamp", -1).limit(1)
    )[0]
    gps["fx"] = int(last_doc["data"])

    return {
        "rtc": "ws://13.38.173.241:3333/app/" + uav.split("uav")[1],
        "status": status,
        "battery": battery,
        "gps": gps,
    }
