from datetime import datetime

import schedule

from app.lib.mongodb import mongodb


fake_data = {
    "uav3": {
        "bat": {
            "id": {
                "value": 1,
                "next_value_diff": 0,
            },
            "pt": {
                "value": 3,
                "next_value_diff": 0,
            },
            "vl": {
                "value": 20,
                "next_value_diff": 0,
            },
        },
        "armed": {
            "value": False,
        },
        "state": {
            "value": "4",
        },
        "in_air": {
            "value": False,
        },
        "gps": {
            "lat": {
                "value": 1.1,
                "next_value_diff": 0,
            },
            "lon": {
                "value": 1.1,
                "next_value_diff": 0,
            },
            "abs": {
                "value": 10,
                "next_value_diff": 0,
            },
            "ns": {
                "value": 3,
                "next_value_diff": 0,
            },
            "fx": {
                "value": 19,
                "next_value_diff": 0,
            },
        },
    },
    "uav4": {
        "bat": {
            "id": {
                "value": 1,
                "next_value_diff": 0,
            },
            "pt": {
                "value": 3,
                "next_value_diff": 0,
            },
            "vl": {
                "value": 15,
                "next_value_diff": -0.01,
            },
        },
        "armed": {
            "value": True,
        },
        "state": {
            "value": "4",
        },
        "in_air": {
            "value": True,
        },
        "gps": {
            "lat": {
                "value": -1.01,
                "next_value_diff": 0.01,
            },
            "lon": {
                "value": 0.01,
                "next_value_diff": -0.03,
            },
            "abs": {
                "value": 10,
                "next_value_diff": 0,
            },
            "ns": {
                "value": 3,
                "next_value_diff": 0,
            },
            "fx": {
                "value": 19,
                "next_value_diff": 0,
            },
        },
    },
    "uav5": {
        "bat": {
            "id": {
                "value": 1,
                "next_value_diff": 0,
            },
            "pt": {
                "value": 3,
                "next_value_diff": 0,
            },
            "vl": {
                "value": 12,
                "next_value_diff": 0,
            },
        },
        "armed": {
            "value": True,
        },
        "state": {
            "value": "4",
        },
        "in_air": {
            "value": False,
        },
        "gps": {
            "lat": {
                "value": -0.001,
                "next_value_diff": 0,
            },
            "lon": {
                "value": 15.0001,
                "next_value_diff": 0,
            },
            "abs": {
                "value": 10,
                "next_value_diff": 0,
            },
            "ns": {
                "value": 3,
                "next_value_diff": 0,
            },
            "fx": {
                "value": 19,
                "next_value_diff": 0,
            },
        },
    },
    "uav6": {
        "bat": {
            "id": {
                "value": 1,
                "next_value_diff": 0,
            },
            "pt": {
                "value": 3,
                "next_value_diff": 0,
            },
            "vl": {
                "value": 25,
                "next_value_diff": -0.01,
            },
        },
        "armed": {
            "value": False,
        },
        "state": {
            "value": "4",
        },
        "in_air": {
            "value": True,
        },
        "gps": {
            "lat": {
                "value": -12.001,
                "next_value_diff": 0.001,
            },
            "lon": {
                "value": 12.0001,
                "next_value_diff": -0.001,
            },
            "abs": {
                "value": 10,
                "next_value_diff": 0,
            },
            "ns": {
                "value": 3,
                "next_value_diff": 0,
            },
            "fx": {
                "value": 19,
                "next_value_diff": 0,
            },
        },
    },
    "uav7": {
        "bat": {
            "id": {
                "value": 1,
                "next_value_diff": 0,
            },
            "pt": {
                "value": 3,
                "next_value_diff": 0,
            },
            "vl": {
                "value": 22,
                "next_value_diff": -0.001,
            },
        },
        "armed": {
            "value": False,
        },
        "state": {
            "value": "4",
        },
        "in_air": {
            "value": True,
        },
        "gps": {
            "lat": {
                "value": -11.001,
                "next_value_diff": 0.01,
            },
            "lon": {
                "value": 4.0001,
                "next_value_diff": -0.004,
            },
            "abs": {
                "value": 10,
                "next_value_diff": 0,
            },
            "ns": {
                "value": 3,
                "next_value_diff": 0,
            },
            "fx": {
                "value": 19,
                "next_value_diff": 0,
            },
        },
    },
}


def start_fake_uavs_data_filling():
    schedule.every(1).seconds.do(_fill_data)


def _fill_data():
    for uav in fake_data.keys():
        for collection in fake_data[uav].keys():
            for type in fake_data[uav][collection].keys():
                if type == "value":
                    document = {
                        "uav": uav,
                        "timestamp": datetime.now(),
                        "type": None,
                        "data": fake_data[uav][collection][type],
                    }

                    mongodb[collection].insert_one(document)
                else:
                    document = {
                        "uav": uav,
                        "timestamp": datetime.now(),
                        "type": type,
                        "data": fake_data[uav][collection][type]["value"],
                    }

                    fake_data[uav][collection][type]["value"] += fake_data[uav][
                        collection
                    ][type]["next_value_diff"]

                    if fake_data[uav][collection][type]["value"] <= 0:
                        fake_data[uav][collection][type]["value"] = 30

                    mongodb[collection].insert_one(document)
