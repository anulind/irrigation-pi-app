import board
import busio
import adafruit_am2320
import devices.mqtt_methods as mqtt_methods
import logging

# Humidity and temperature sensor
class AM2320(mqtt_methods.Mixin):
    def __init__(self):
        logging.debug("[AM2320] Initializing sensor...")
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_am2320.AM2320(self.i2c)
        logging.debug("[AM2320] configuration complete")

    def read(self):
        logging.debug("[AM2320] reading sensor")
        temperature = self.sensor.temperature
        humidity = self.sensor.relative_humidity

        logging.debug("[AM2320] temperature = {}".format(temperature))
        logging.debug("[AM2320] humidity = {}".format(humidity))

        return {
            'temperature': temperature,
            'humidity': humidity
        }
