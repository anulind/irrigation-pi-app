import queue
import pytz
import worker.read_sensors as read_sensors
import worker.handle_request as handle_request
from datetime import datetime
from utils import json_dumps

class Worker(read_sensors.Mixin, handle_request.Mixin):
    def __init__(self, devices, mqtt):
        self.queue = queue.Queue()
        self.devices = devices
        self.mqtt = mqtt

    # Append new job to the queue
    def append(self, name, payload={}):
        self.queue.put({
            "name": name,
            "payload": payload,
        })

    def cancel(self):
        # Remove any future jobs
        with self.queue.mutex:
            self.queue.queue.clear()
        # Interrupt any ongoing processes
        self.devices.close_relays(self.mqtt)

    def work(self):
        try:
            job = self.queue.get(False)
            name = job["name"]

            if name == "read_sensors":
                self.read_sensors()
                self.devices.close_relays(self.mqtt)
            elif name == "handle_request":
                self.handle_request(job["payload"])
                self.devices.close_relays(self.mqtt)
            else:
                print("Task '{}' not recongnised, ignoring...".format(name))
                return

        except queue.Empty:
            return

    def print_error(self, e, message):
        print(message)
        print(type(e))
        print(e.args)
        print(e)
