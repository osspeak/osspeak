import tkinter as tk
import threading
from interfaces.gui.app import Application

class GuiManager:

    def __init__(self):
        pass

    def start(self):
        self.app = Application()
        self.app.widget.protocol("WM_DELETE_WINDOW", self.on_close)
        self.app.widget.mainloop()

    def on_close(self):
        print('close')
        self.app.shutdown()
        