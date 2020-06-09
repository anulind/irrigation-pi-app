from datetime import datetime
import pytz

class Mixin:
    def periodic_reading(self):
        print("[periodic reading]: getting values...")
        timestamp = datetime.now(pytz.timezone('Europe/Stockholm'))

        try:
            self.devices.AM2320.read_and_publish(self.mqtt, timestamp=timestamp)
        except Exception as inst:
            self.print_error(inst, "[periodic reading]: AM2320 failed")

        try:
            self.devices.BMP280.read_and_publish(self.mqtt, timestamp=timestamp)
        except Exception as inst:
            self.print_error(inst, "[periodic reading]: BMP280 failed")

        try:
            self.devices.TSL2561.read_and_publish(self.mqtt, timestamp=timestamp)
        except Exception as inst:
            self.print_error(inst, "[periodic reading]: TSL2561 failed")

        print("[periodic reading]: job done")
