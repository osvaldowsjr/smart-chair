from model.smartChairModel import chairData


# Controle das informações retiradas do json
class dataManager:
    def __init__(self, data):
        self.data = chairData(data)

    def checkPresence(self):
        return self.data.presence

    def getHumidity(self):
        return self.data.humidity

    def getTemperature(self):
        return self.data.temp

    def getLuminosity(self):
        return self.data.luminosity

    def getTime(self):
        return self.data.time
