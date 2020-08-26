import tkinter as tk

from viewModel.dataManager import dataManager


class Application(tk.Frame, dataManager):
    def __init__(self, master=None):
        super().__init__(master)
        self.titleTemp = tk.Label()
        self.titleHum = tk.Label()
        self.temp = tk.Label()
        self.hum = tk.Label()
        self.dataManager = dataManager
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.titleTemp.text = 'Temperatura:'
