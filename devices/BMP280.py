import board
import busio
import adafruit_bmp280
import devices.mqtt_methods as mqtt_methods
import logging

class BMP280(mqtt_methods.Mixin):
    def __init__(self):
        logging.debug("[BMP280] Initializing sensor...")
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x76)
        self.sensor.sea_level_pressure = 1013.25
        logging.debug("[BMP280] configuration complete")

    def read(self):
        logging.debug("[BMP280] reading sensor")
        temperature = self.sensor.temperature
        pressure = self.sensor.pressure

        logging.debug("[BMP280] temperature = {}".format(temperature))
        logging.debug("[BMP280] pressure = {}".format(pressure))

        return {
            'temperature': round(temperature, 2),
            'pressure': round(pressure, 2)
        }
