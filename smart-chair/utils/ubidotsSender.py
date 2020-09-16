from time import sleep

from viewModel.dataManager import dataManager
import requests


# Classe que controla o envio de informações para o Ubidots
class UbidotsSender:
    def __init__(self, dm: dataManager):
        self.url = "https://things.ubidots.com/api/v1.6/devices/cadeira/"
        self.headers = {"X-Auth-Token": "BBFF-vRwtoHA1ToTiggR6hmF1V2xvuHEYoL",
                        "Content-Type": "application/json"}
        self.json = self.formatPayload(dm)

    def post(self):
        status = 400
        attempts = 0
        while status >= 400 and attempts <= 5:
            req = requests.post(url=self.url, headers=self.headers, json=self.json)
            status = req.status_code
            attempts += 1
        if status >= 400:
            print("[ERROR] Could not send data after 5 attempts, please check \
                    your token credentials and internet connection")
            return False

        print("[INFO] request made properly, your device is updated")
        return True

    @staticmethod
    def formatPayload(dm: dataManager):
        valuePresence = 0
        if dm.checkPresence():
            valuePresence = 1

        payload = {
            "humidade": dm.getHumidity(),
            "temperatura": dm.getTemperature(),
            "presenca": valuePresence
        }
        return payload
