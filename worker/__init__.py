import queue
import pytz
import worker.periodic_reading as periodic_reading
import worker.handle_request as handle_request
from datetime import datetime
from utils import json_dumps

class Worker(periodic_reading.Mixin, handle_request.Mixin):
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

    def work(self):
        try:
            job = self.queue.get(False)
            name = job["name"]

            if name == "periodic_reading":
                self.periodic_reading()
            elif name == "handle_request":
                self.handle_request(job["payload"])
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
