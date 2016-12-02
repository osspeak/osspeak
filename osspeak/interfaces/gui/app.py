from interfaces.gui import component
import tkinter as tk

class Application(component.Component):

    def __init__(self):
        self.widget = tk.Tk()
        w = tk.Label(self.widget, text="Hello, world!")
        w.pack()

    def shutdown(self):
        self.widget.destroy()