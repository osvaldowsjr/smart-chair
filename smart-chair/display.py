import os.path
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from random import uniform
from stopwatch import Stopwatch
from viewModel.dataManager import dataManager
from viewModel.timeManager import timeManager
from viewModel.temperatureManager import tempManager
from view.interface import Application
import tkinter
import gpiozero

# receiver = Receiver(port="COM4", baudrate=115200,
#                   bytesize=8, timeout=2)

def dealAlarm(data_manager: dataManager, timer_idle: Stopwatch, timer_stand):
    alarm_manager = timeManager(data_manager, timer_idle, timer_stand)
    alarm_manager.tryStartTimer()
    alarm_manager.tryStopTimer()
    if alarm_manager.shouldAlarm():
        # led.on()
        print("led on")
        delay = input("Adiar? (s/n)? ")
        if delay.upper() == 'S':
            alarm_manager.delayTimer()
            print("led off")
        else:
            print("led on")


def dealTemp(temp: float):
    temp_manager = tempManager(temp)
    print(temp_manager.getDisplayMsg())


def bt0():
    randH = uniform(0.0, 10.0)
    randT = uniform(9.0, 40.0)
    randL = uniform(0.0, 5.0)
    new_json = '{{"humidity":{0},"temperature": {1}, "luminosity": {2}, "presence": {3}, "time": {4}}}'.format(
        randH,
        randT,
        randL,
        "false",
        1200)
    print(new_json)
    return dataManager(new_json)


if __name__ == '__main__':
    sw = Stopwatch()
    sw.stop()
    sw2 = Stopwatch()
    sw2.stop()
    root = tkinter.Tk()
    view = Application(root)
    view.mainloop()
    # led = gpiozero.LED(17)
    while 1:
        # info = receiver.receiveInfo()
        # dm = dataManager(info)
        dm = bt0()
        view.button0(dm=dm)
        dealAlarm(dm, sw, sw2)
        dealTemp(dm.getTemperature())
