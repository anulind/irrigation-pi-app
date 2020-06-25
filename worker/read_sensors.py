import pytz
from datetime import datetime
import logging

class Mixin:
    def read_sensor(self, device, pin=None, timestamp=None, origin=None):
        try:
            getattr(self.devices, device).read_and_publish(
                self.mqtt,
                pin=pin,
                timestamp=timestamp,
                origin=origin,
            )
        except Exception as inst:
            self.print_error(inst, "[worker]: {} failed".format(device))

    def read_sensors(self, origin=None):
        logging.debug("[worker]: reading sensors...")
        timestamp = datetime.now(pytz.timezone('Europe/Stockholm'))

        sensors = [
            'AM2320', 'BMP280', 'HCSR04', 'TSL2561',
            {'device': 'MCP23017', 'pin': 'got_water'},
            {'device': 'MCP3008', 'pin': 'soil_moisture_1'},
            {'device': 'MCP3008', 'pin': 'soil_moisture_2'},
            {'device': 'MCP3008', 'pin': 'soil_moisture_3'},
            {'device': 'MCP3008', 'pin': 'soil_moisture_4'},
            {'device': 'MCP3008', 'pin': 'temperature'},
        ]
        for sensor in sensors:
            if isinstance(sensor, str):
                self.read_sensor(sensor, timestamp=timestamp, origin=origin)
            else:
                self.read_sensor(
                    sensor['device'],
                    pin=sensor.get('pin'),
                    timestamp=timestamp,
                    origin=origin
                )
