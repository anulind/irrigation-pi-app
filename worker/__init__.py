import queue
import worker.methods.periodic_reading as periodic_reading

class Worker:
    def __init__(self, devices, mqtt):
        self.queue = queue.Queue()
        self.devices = devices
        self.mqtt = mqtt

    # Append new job to the queue
    def append(self, name):
        self.queue.put({
            "name": name,
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
                periodic_reading.run(self.devices, self.mqtt)
            else:
                print("Task '{}' not recongnised, ignoring...".format(name))
                return

        except queue.Empty:
            return
