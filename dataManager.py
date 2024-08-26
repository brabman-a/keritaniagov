import json
import threading

Stream = open("govdata.json", "r+")
Data = json.load(Stream)

queue = []

def WriteUser(name: str, key: str, value):
    def operation():
        global Stream
        global Data
        logins = Data['logins']
        user = logins.get(name)
        if (user):
            logins[name][key] = value
        json.dump(Data, Stream)
    operation()
    # queue.append(operation)

def GetUser(name: str):
    return Data['users'].get(name)
