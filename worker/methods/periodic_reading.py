import json

def run(devices, mqtt):
    print("[periodic reading]: getting values...")

    # Read sensors and publish values
    humidity = devices.AM2320.read()
    mqtt.publish('AM2320', json.dumps(humidity))

    pressure = devices.BMP280.read()
    mqtt.publish('BMP280', json.dumps(pressure))

    light = devices.TSL2561.read()
    mqtt.publish('TSL2561', json.dumps(light))

    print("[periodic reading]: job done")
