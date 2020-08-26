import json


class chairData:
    def __init__(self, object):
        self.jsonData = json.loads(object)
        self.humidity = self.jsonData['humidity']
        self.temp = self.jsonData['temperature']
        self.luminosity = self.jsonData['luminosity']
        self.presence = self.jsonData['presence']
        self.time = self.jsonData['time']
