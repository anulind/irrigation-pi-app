import board
import busio
import adafruit_am2320
from random import random

# Humidity and temperature sensor
class AM2320:
    def __init__(self):
        print("[AM2320] Initializing sensor...")
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_am2320.AM2320(self.i2c)
        print("[AM2320] configuration complete")

    def read(self):
        print("[AM2320] reading sensor")
        temperature = self.sensor.temperature,
        humidity = self.sensor.relative_humidity

        print("[AM2320] temperature = {}".format(temperature))
        print("[AM2320] humidity = {}".format(humidity))

        return {
            'temperature': temperature,
            'humidity': humidity
        }
