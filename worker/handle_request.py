from utils import json_dumps

event_topic = 'pi/events'

class Mixin:
    def handle_request(self, message):
        action = message.get('action')
        requestId = message.get('requestId')
        payload = message.get('payload')
        print("[handle request]: processing request id = {}, action = {}, payload = {}".format(requestId, action, payload))
        self.mqtt.publish(event_topic, json_dumps({
            "requestId": requestId,
            "status": "initiated",
        }))

        try:
            if action == "read":
                device = payload.get('device', None)
                if device == "MCP23017" or device == "MCP3008":
                    self.read_and_publish(device, pin=payload['pin'], origin=requestId)
                else:
                    self.read_and_publish(device, origin=requestId)

                self.mqtt.publish(event_topic, json_dumps({
                    "requestId": requestId,
                    "status": "completed",
                }))

            elif action == "set":
                device = payload['device']
                pin = payload.get('pin')
                target = payload['target']
                getattr(self.devices, device).set_value(pin, target)
                self.mqtt.publish(event_topic, json_dumps({
                    "requestId": requestId,
                    "status": "completed",
                }))

            elif action == "run":
                device = payload['device']
                pin = payload.get('pin')
                duration = payload['duration']
                getattr(self.devices, device).run(pin, { 'duration': duration })
                self.mqtt.publish(event_topic, json_dumps({
                    "requestId": requestId,
                    "status": "completed",
                }))

            else:
                print("[handle request]: Request {} not recognized".format(action))
                self.mqtt.publish(event_topic, json_dumps({
                    "requestId": requestId,
                    "status": "rejected",
                    "error": "Invalid payload",
                }))

        except Exception as e:
            print("[handle request]: unexpected error occured")
            print(type(e))
            print(e.args)
            print(e)
            self.mqtt.publish(event_topic, json_dumps({
                "requestId": requestId,
                "status": "failed",
                "error": str(e),
            }))

        print("[handle request]: job done")
