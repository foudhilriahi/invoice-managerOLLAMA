import json

def is_valid_json(text):
    try:
        data = json.loads(text)
        return True, data
    except json.JSONDecodeError:
        return False, None
