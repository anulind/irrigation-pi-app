import RPi.GPIO as GPIO
import time
import devices.mqtt_methods as mqtt_methods
import logging

class HCSR04(mqtt_methods.Mixin):
    def __init__(self):
        logging.debug("[HCSR04] Initializing sensor...")
        self.GPIO = GPIO
        GPIO.setmode(GPIO.BCM)
        self.TRIG = 23
        self.ECHO = 24
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.output(self.TRIG, False)
        logging.debug("[HCSR04] configuration complete")

    def read(self):
        # Number of attempts to read sensor before giving up
        n = 20
        # Number of nonzero readings that we want to get
        m = 10
        # Number of nonzero readings that's good enough
        k = 5

        result = []
        logging.debug("[HCSR04] reading sensor:")
        for _ in range(0, n):
            try:
                value = self._raw_read()
                logging.debug(">>>> {}".format(value))
                if value > 0:
                    result.append(value)
                if len(result) >= m:
                    break
                time.sleep(0.5)

            except Exception:
                logging.exception(">>>> [HCSR04] fail")

        # If we didn't get enough nonzero readings
        if len(result) < k:
            raise Exception("Got {} nonzero readings from HCSR04".format(len(result)))

        # Calculate average
        value = round(sum(result)/len(result), 1)
        logging.debug("[HCSR04] range = {}".format(value))

        return {
            'range': value
        }

    def _raw_read(self):
        self.GPIO.output(self.TRIG, False)
        # "Waiting For Sensor To Settle"
        time.sleep(2)
        self.GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        self.GPIO.output(self.TRIG, False)
        while self.GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()
        while self.GPIO.input(self.ECHO) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return distance

    def cleanup(self):
        self.GPIO.cleanup()
