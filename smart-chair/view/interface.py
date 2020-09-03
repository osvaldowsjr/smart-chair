import tkinter as tk
from random import uniform

from viewModel.dataManager import dataManager


class aa(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.dm = dataManager('{"humidity":0,"temperature": 1, "luminosity": 2, "presence": false, "time": 1200}')
        self.tempVar = tk.StringVar()
        self.humVar = tk.StringVar()
        self.titleTemp = tk.Label(master, text='Temperatura:', bg="red", fg="white")
        self.temp = tk.Label(master, textvariable=self.tempVar, bg="red", fg="white")

        self.titleHum = tk.Label(master, text='Umidade:', bg="red", fg="white")
        self.hum = tk.Label(master, textvariable=self.humVar, bg="green", fg="white")

        self.randButton0 = tk.Button(master, text="0", bg="green", command=self.update_widgets())
        self.randButton1 = tk.Button(master, text="1", bg="red")

        self.dataManager = dataManager
        self.createWidgets()

    def createWidgets(self):
        self.titleHum.pack(fill=tk.X)
        self.hum.pack(fill=tk.X)
        self.titleTemp.pack(fill=tk.X)
        self.temp.pack(fill=tk.X)
        self.randButton0.pack(fill=tk.X)
        self.randButton1.pack(fill=tk.X)

    def update_widgets(self):
        self.tempVar.set(self.dm.getTemperature())
        self.humVar.set(self.dm.getHumidity())

    def button0(self, dm: dataManager):
        self.dm = dm
