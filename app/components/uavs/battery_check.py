from app.lib.mongodb import mongodb
from app.lib.broadcaster import send_notification

def check_battery_stats():
    print("Checking Battery Stats")
    uavs = mongodb['bat'].distinct('uav')
    for uav in uavs:
        last_doc = mongodb['bat'].find({'uav': uav, 'type': 'vl'}).sort('timestamp', -1).limit(1)[0]
        voltage_level = float(last_doc['data'])
        if voltage_level < 3.7:
            send_notification(uav, 'battery_low', voltage_level)