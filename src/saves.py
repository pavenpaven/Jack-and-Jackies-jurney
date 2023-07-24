import json

def save(filename):
    txt = json.dumps(state)
    with open("filename", "r") as fil:
        fil.write(txt)

def load(filename):
    with open(filename) as fil:
        txt = fil.read()
    Save.state = json.loads(txt)

class Save:
    state = {}
