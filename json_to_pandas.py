import json

file = "data.json"

def load_json(file):
    with open(file, encoding="utf-8") as f:
        data = json.load(f)
    return data


json_data = load_json(file)
print(type(json_data))