import os.path
import sys
import tkinter
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from stopwatch import Stopwatch
from viewModel.timeManager import timeManager
from viewModel.temperatureManager import tempManager
from random import uniform
import tkinter as tk
from viewModel.dataManager import dataManager


# receiver = Receiver(port="COM4", baudrate=115200,
#                   bytesize=8, timeout=2)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.dm = dataManager('{"humidity":0,"temperature": 1, "luminosity": 2, "presence": false, "time": 1200}')
        self.presence = 0

        self.tempVar = tk.StringVar()
        self.humVar = tk.StringVar()
        self.delayVar = tk.StringVar()

        self.titleTemp = tk.Label(master, text='Temperatura:', bg="red", fg="white")
        self.temp = tk.Label(master, textvariable=self.tempVar, bg="red", fg="white")

        self.titleHum = tk.Label(master, text='Umidade:', bg="red", fg="white")
        self.hum = tk.Label(master, textvariable=self.humVar, bg="green", fg="white")

        # TEMP
        self.randButton0 = tk.Button(master, text="0", bg="green", command=self.update_widgets0)
        self.randButton1 = tk.Button(master, text="1", bg="red", command=self.update_widgets1)
        #

        self.adiarBt = tk.Button(master, text="Adiar", bg="green", command=self.delay)
        self.desligarBt = tk.Button(master, text="Desligar", bg="red", command=self.delayVar.set("N"))

        self.dataManager = dataManager
        self.createWidgets()

    def createWidgets(self):
        self.titleHum.pack(fill=tk.X)
        self.hum.pack(fill=tk.X)
        self.titleTemp.pack(fill=tk.X)
        self.temp.pack(fill=tk.X)
        self.randButton0.pack(fill=tk.X)
        self.randButton1.pack(fill=tk.X)
        self.adiarBt.pack(fill=tk.X)
        self.desligarBt.pack(fill=tk.X)

    def update_widgets0(self):
        self.presence = 0

    def update_widgets1(self):
        self.presence = 1

    def delay(self, alarm_manager):
        alarm_manager.delayTimer()
        self.delayVar.set("S")
        print("led off")

    def dealAlarm(self, timer_idle: Stopwatch, timer_stand):
        alarm_manager = timeManager(self.dm, timer_idle, timer_stand)
        alarm_manager.tryStartTimer()
        alarm_manager.tryStopTimer()
        if alarm_manager.shouldAlarm():
            print('alarme on')
            print(self.delayVar.get())
            if self.delayVar.get().upper() == 'S':
                self.delay(alarm_manager=alarm_manager)
                print('alarme off')
            elif self.delayVar.get().upper() == 'N':
                print('alarme on 2')

    def dealTemp(self):
        temp_manager = tempManager(self.dm.getTemperature())
        print(temp_manager.getDisplayMsg())

    def update_dm(self, json):
        self.dm = dataManager(json)
        self.tempVar.set(self.dm.getTemperature())
        self.humVar.set(self.dm.getHumidity())


root = tkinter.Tk()
view = Application(root)

# led = gpiozero.LED(17)
sw = Stopwatch()
sw.stop()
sw2 = Stopwatch()
sw2.stop()


def abc():
    # info = receiver.receiveInfo()
    randH = uniform(0.0, 10.0)
    randT = uniform(9.0, 40.0)
    randL = uniform(0.0, 5.0)
    presence = ['false', 'true']
    new_json = '{{"humidity":{0},"temperature": {1}, "luminosity": {2}, "presence": {3}, "time": {4}}}'.format(
        randH,
        randT,
        randL,
        presence[view.presence],
        1200)
    print(new_json)
    view.update_dm(new_json)
    view.dealAlarm(sw, sw2)
    root.after(1000, abc)


root.after(1000, abc)
view.mainloop()
