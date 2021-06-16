import json


def success(obj):
    return json.dumps(obj), 200, {'Content-Type': 'application/json'}


def error(message):
    return json.dumps({'error': message}), 500, {'Content-Type': 'application/json'}