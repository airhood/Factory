import json

def load_chip(filename):
    with open(filename) as f:
        data = json.load(f)
    f.close()
    return data