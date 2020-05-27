from utils import json_dumps
from datetime import datetime
import pytz

def build_message(timestamp, data, key):
    return json_dumps({
        'timestamp': timestamp,
        'triggeredBy': "pi",
        'data': data[key],
    })

def run(devices, mqtt):
    print("[periodic reading]: getting values...")
    timestamp = datetime.now(pytz.timezone('Europe/Stockholm'))

    try:
        reading = devices.AM2320.read()
        mqtt.publish('pi/AM2320/data/humidity',
                    build_message(timestamp, reading, 'humidity'))
        mqtt.publish('pi/AM2320/data/temperature',
                    build_message(timestamp, reading, 'temperature'))
    except Exception as inst:
        print("[periodic reading]: AM2320 failed")
        print(type(inst))
        print(inst.args)
        print(inst)

    try:
        reading = devices.BMP280.read()
        mqtt.publish('pi/BMP280/data/pressure',
                    build_message(timestamp, reading, 'pressure'))
        mqtt.publish('pi/BMP280/data/temperature',
                    build_message(timestamp, reading, 'temperature'))
    except Exception as inst:
        print("[periodic reading]: BMP280 failed")
        print(type(inst))
        print(inst.args)
        print(inst)

    try:
        reading = devices.TSL2561.read()
        mqtt.publish('pi/TSL2561/data/light',
                    build_message(timestamp, reading, 'light'))
    except Exception as inst:
        print("[periodic reading]: TSL2561 failed")
        print(type(inst))
        print(inst.args)
        print(inst)

    print("[periodic reading]: job done")
