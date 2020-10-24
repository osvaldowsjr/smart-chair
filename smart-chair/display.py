import os.path
import sys
import tkinter
from datetime import datetime
import tkinter as tk
import threading
import gpiozero

# Imports custom - Start Region

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from stopwatch import Stopwatch
from viewModel.timeManager import timeManager
from viewModel.temperatureManager import tempManager
from random import uniform
from utils.ubidotsSender import UbidotsSender
from viewModel.dataManager import dataManager
from utils.serialreceiver import Receiver

# End Region
# ------------------------------------------------------------------------------------------


# Criação do layout - Start Region
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.dm = dataManager('{"humidity":0,"temperature": 1, "luminosity": 2, "presence": false, "time": 1200}')
        self.presence = 0
        self.alarmTime = 5.00

        self.tempVar = tk.StringVar()
        self.humVar = tk.StringVar()
        self.delayVar = tk.StringVar(value="Off")

        self.titleTemp = tk.Label(master, text='Temperatura:', bg="red", fg="white")
        self.temp = tk.Label(master, textvariable=self.tempVar, bg="red", fg="white")

        self.titleHum = tk.Label(master, text='Umidade:', bg="red", fg="white")
        self.hum = tk.Label(master, textvariable=self.humVar, bg="green", fg="white")

        # TEMP
        self.randButton0 = tk.Button(master, text="0", bg="green", command=self.update_widgets0)
        self.randButton1 = tk.Button(master, text="1", bg="red", command=self.update_widgets1)
        #

        self.adiarBt = tk.Button(master, text="Adiar", bg="green", command=self.setDelayVar)
        self.desligarBt = tk.Button(master, text="Desligar", bg="red", command=self.setDelayVarOff)

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

    # End Region
    # ------------------------------------------------------------------------------------------
    # Funções para interação com o display - Start Region

    def update_widgets0(self):
        self.presence = 0

    def update_widgets1(self):
        self.presence = 1

    def setDelayVar(self):
        self.delayVar.set("Adiar")

    def setDelayVarOff(self):
        self.delayVar.set("Desligar")

    # End Region
    # ------------------------------------------------------------------------------------------
    # Funções de alarme e led - Start Region

    def dealAlarm(self, timer_idle: Stopwatch, timer_stand):
        alarm_manager = timeManager(self.dm, timer_idle, timer_stand)
        alarm_manager.tryStartTimer()
        alarm_manager.tryStopTimer()
        if not self.dm.checkPresence():
            self.setAlarmInitial(alarm_manager)
        if alarm_manager.shouldAlarm(self.alarmTime):
            if self.delayVar.get() == "Off":
                led.on()
                print("alarm On - Condição off")
                self.alarmTime += 1.0
            elif self.delayVar.get() == "Desligar":
                self.turnOffAlarm(alarm_manager)
            elif self.delayVar.get() == "Adiar":
                self.delayAlarm(alarm_manager)
            else:
                print("alarm Off - Sem condiçoes")
                led.off()

    def turnOffAlarm(self, alarmManager: timeManager):
        alarmManager.turnOffAlarm()
        self.alarmTime = 5.0
        print("alarm off - desligar")
        led.off()
        self.delayVar.set("Off")

    def delayAlarm(self, alarmManager: timeManager):
        alarmManager.turnOffAlarm()
        self.alarmTime += 5.0
        print("alarm off - Adiar")
        led.off()
        self.delayVar.set("Off")

    def setAlarmInitial(self, alarmManager: timeManager):
        print("Alarm off - initial")
        self.alarmTime = 5.0
        led.off()
        alarmManager.turnOffAlarm()

    # End Region
    # ------------------------------------------------------------------------------------------
    # Funções para controle de temperatura - Start Region

    def dealTemp(self):
        temp_manager = tempManager(self.dm.getTemperature())
        print(temp_manager.getDisplayMsg())

    # End Region
    # ------------------------------------------------------------------------------------------
    # Funçoes de controle de informação - Start Region

    def update_dm(self, json):
        self.dm = dataManager(json)
        self.tempVar.set("%.2f" % (self.dm.getTemperature()))
        self.humVar.set("%.2f" % (self.dm.getHumidity()))
        t = threading.Thread(target=self.sendInfo)
        t.start()

    def sendInfo(self):
        UbidotsSender(self.dm).post()


# End Region
# ------------------------------------------------------------------------------------------
# Criações das instancias - Start Region

root = tkinter.Tk()
view = Application(root)

led = gpiozero.LED(17)
sw = Stopwatch()
sw.stop()
sw2 = Stopwatch()
sw2.stop()

receiver = Receiver(port="/dev/ttyACM0", baudrate=9600,
                    bytesize=8, timeout=2)

# End Region
# ------------------------------------------------------------------------------------------
# Geração de JSON fake - Start Region

def generateJson():
    info = receiver.receiveInfo()
    randL = uniform(0.0, 5.0)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    info.replace("null", randL)
    info.replace('queijo', current_time)
    print(info)
    view.update_dm(info)
    view.dealAlarm(sw, sw2)
    view.dealTemp()
    root.after(5000, generateJson)


# End Region
# ------------------------------------------------------------------------------------------
# Finalização da cadeira - Start Region

def turnOffChair():
    led.off()
    root.destroy()
    sys.exit("Obrigado por usar a cadeira S2")


# End Region
# ------------------------------------------------------------------------------------------
# Main loop - Start Region

root.after(1000, generateJson)
root.protocol("WM_DELETE_WINDOW", turnOffChair)
view.mainloop()

# End Region
