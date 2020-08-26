import sys

sys.path.append('../viewModel/')
sys.path.append('../view/')
sys.path.append('../model/')
sys.path.append('../utils/')
from random import uniform
from stopwatch import Stopwatch
from viewModel.dataManager import dataManager
from viewModel.timeManager import timeManager
from viewModel.temperatureManager import tempManager
import gpiozero


# receiver = Receiver(port="COM4", baudrate=115200,
#                   bytesize=8, timeout=2)

def dealAlarm(data_manager: dataManager, timer_idle: Stopwatch, timer_stand):
    alarm_manager = timeManager(data_manager, timer_idle,timer_stand)
    alarm_manager.tryStartTimer()
    alarm_manager.tryStopTimer()
    if alarm_manager.shouldAlarm():
        print("alarme!")
        delay = input("Adiar? (s/n)? ")
        if delay.upper() == 'S':
            alarm_manager.delayTimer()
        else:
            led.blink()


def dealTemp(temp: float):
    temp_manager = tempManager(temp)
    print(temp_manager.getDisplayMsg())


if __name__ == '__main__':
    sw = Stopwatch()
    sw.stop()
    sw2 = Stopwatch()
    sw2.stop()
    led = gpiozero.LED(17)
    # root = tk.Tk()
    # app = Application(master=root)
    # app.mainloop()
    while 1:
        # info = receiver.receiveInfo()
        # dm = dataManager(info)
        presence_val = input("Press 0 or 1")
        randH = uniform(0.0, 10.0)
        randT = uniform(9.0, 40.0)
        randL = uniform(0.0, 5.0)
        presence = ["false", "true"]
        new_json = '{{"humidity":{0},"temperature": {1}, "luminosity": {2}, "presence": {3}, "time": {4}}}'.format(
            randH,
            randT,
            randL,
            presence[int(presence_val)],
            1200)
        print(new_json)
        dm = dataManager(new_json)
        dealAlarm(dm, sw,sw2)
        dealTemp(dm.getTemperature())
