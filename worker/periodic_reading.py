from datetime import datetime
import pytz

class Mixin:
    def periodic_reading(self):
        print("[periodic reading]: getting values...")
        timestamp = datetime.now(pytz.timezone('Europe/Stockholm'))

        try:
            self.read_and_publish('AM2320', timestamp=timestamp)
        except Exception as inst:
            self.print_error(inst, "[periodic reading]: AM2320 failed")

        try:
            self.read_and_publish('BMP280', timestamp=timestamp)
        except Exception as inst:
            self.print_error(inst, "[periodic reading]: BMP280 failed")

        try:
            self.read_and_publish('TSL2561', timestamp=timestamp)
        except Exception as inst:
            self.print_error(inst, "[periodic reading]: TSL2561 failed")

        print("[periodic reading]: job done")
