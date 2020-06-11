import queue
import pytz
from datetime import datetime
from utils import json_dumps
import time

class Mixin:
    def build_mqtt_message(self, timestamp=None, origin=None):
        # Generate timestamp if necessary
        if not timestamp:
            timestamp = datetime.now(pytz.timezone('Europe/Stockholm'))

        message = {'timestamp': timestamp}

        # Add origin to message if present
        if origin:
            message['origin'] = origin

        return message

    def read_and_publish(self, mqtt, pin=None, timestamp=None, origin=None):
        print("[mqtt mixin]: reading sensor")

        # If pin is given, send it as an argument
        reading = self.read(pin) if pin else self.read()

        print("[mqtt mixin]: publishing values")
        message = self.build_mqtt_message(timestamp, origin)
        # Each reading is a dict which maps name (e.g. humidity, soil_moisture_1, ...) to value
        # Each value is published on a separate topic
        device_name = type(self).__name__
        for name, value in reading.items():
            mqtt.publish(
                "pi/sensors/{}/{}".format(device_name, name),
                json_dumps({
                    **message,
                    'data': value,
                })
            )
        print("[mqtt mixin]: done reading")

    def set_and_publish(self, mqtt, pin, target, timestamp=None, origin=None):
        print("[mqtt mixin]: setting value")
        self.set_value(pin, target)

        print("[mqtt mixin]: publishing value")
        message = self.build_mqtt_message(timestamp, origin)
        _, pin_name = self.get_pin_info(pin)
        device_name = type(self).__name__
        # Publish pin state (using pin name and not number)
        mqtt.publish(
            "pi/sensors/{}/{}".format(device_name, pin_name),
            json_dumps({
                **message,
                'data': target,
            })
        )
        print("[mqtt mixin]: target set")

    def run_and_publish(self, mqtt, pin, duration, timestamp=None, origin=None):
        print("[mqtt mixin] turning {} on for {} seconds".format(pin, duration))

        # Validate duration
        max_duration = 30
        if not isinstance(duration, int):
            raise ValueError("Duration must be integer (given: {})".format(duration))
        if duration > max_duration:
            raise ValueError("Duration can be at most {}".format(max_duration))
        if duration < 1:
            raise ValueError("Duration must be at least 1")

        # Turn relay on
        self.set_and_publish(mqtt, pin, 1, timestamp=timestamp, origin=origin)
        # Wait for `duration` seconds
        print("[mqtt mixin] {} turned on, sleeping for {} seconds".format(pin, duration))
        time.sleep(duration)

        # Check that relay is on
        status = self.read(pin)[pin]
        if status == 0:
            raise Exception("Failed to complete task - could not turn on relay or job cancelled")

        # Turn relay off
        self.set_and_publish(mqtt, pin, 0, timestamp=timestamp, origin=origin)
        print("[mqtt mixin] job complete")
