import json

def serialize(data):
    return json.dumps(data)

def deserialize(data):
    return json.loads(data)

