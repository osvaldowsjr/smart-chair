from viewModel.dataManager import dataManager
from stopwatch import Stopwatch


class timeManager:
    def __init__(self, dm: dataManager, sw: Stopwatch, sw2: Stopwatch):
        self.dm = dm
        self.sw = sw
        self.sw2 = sw2

    def tryStartTimer(self):
        if self.dm.checkPresence() and not self.sw.running:
            if self.sw2.duration <= 10.00 and not self.sw.running:
                print("Tempo insuficiente para melhorar a circulação")
            self.sw.start()
            self.sw2.stop()
            self.sw2.reset()

    def tryStopTimer(self):
        if not self.dm.checkPresence() and self.sw.running:
            self.sw.stop()
            self.sw.reset()
            self.sw2.start()
            print("usuário saiu")

    def shouldAlarm(self, duration: float):
        return self.sw.duration >= duration

    def turnOffAlarm(self):
        self.sw.stop()
        self.sw.reset()
