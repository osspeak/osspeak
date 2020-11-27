import ctypes
import win32gui, win32con

TEXT_FORMAT = win32con.DT_CENTER | win32con.DT_NOCLIP | win32con.DT_SINGLELINE | win32con.DT_VCENTER

class Rectangle:

    def __init__(self, x: int, y: int, width: int, height: int, text=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, device_context_handle):
        x2, y2 = self.x + self.width, self.y + self.height
        win32gui.DrawText(
            device_context_handle,
            self.text,
            -1,
            (self.x, self.y, x2, y2),
            TEXT_FORMAT
        )