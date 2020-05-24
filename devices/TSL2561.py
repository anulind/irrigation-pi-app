import board
import busio
import adafruit_tsl2561
import time

class TSL2561:
    def __init__(self):
        print("[TSL2561] Initializing sensor...")
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the TSL2561 instance, passing in the I2C bus
        self.sensor = adafruit_tsl2561.TSL2561(i2c)

        # Enable the light sensor
        self.sensor.enabled = True
        time.sleep(1)

        # Set gain 0=1x, 1=16x
        self.sensor.gain = 0
        # Set integration time (0=13.7ms, 1=101ms, 2=402ms, or 3=manual)
        self.sensor.integration_time = 1

        print("[TSL2561] configuration complete")

    def read(self):
        print("[TSL2561] reading sensor")

        # Enable and read sensor
        self.sensor.enabled = True
        time.sleep(1)
        lux = self.sensor.lux

        # Disble the light sensor (to save power)
        self.sensor.enabled = False

        if lux is not None:
            print("[TSL2561] Lux = {}".format(lux))
            return {
                'light': round(lux, 2)
            }
        else:
            print("[TSL2561] Lux value is None. Possible sensor underrange or overrange.")
            return {
                'light': None
            }
