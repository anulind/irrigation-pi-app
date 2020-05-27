import json
from datetime import datetime

# Use special converter for datetime, otherwise regular json encoding
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)

def json_dumps(obj):
    return json.dumps(obj, cls=JSONEncoder)
