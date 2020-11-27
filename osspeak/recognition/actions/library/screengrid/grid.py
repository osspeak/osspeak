import string
import keyboard
from . import screencanvas

import threading
import time
import string
import functools
import mouse

ALL_CHARS = string.ascii_lowercase + string.digits

class Grid:

    def __init__(self, x=0, y=0, width=None, height=None, font_color=(0, 0, 0)):
        kw = {}
        if width is not None:
            kw['width'] = width
        if height is not None:
            kw['height'] = height
        self.canvas = screencanvas.ScreenCanvas(x=x, y=y, font_color=font_color, **kw)
        self.selection = ''
        self.centers = {}
        self.keyboard_hook = None
        self._font_color = font_color
        self._xiterable = None
        self._yiterable = None

    @property
    def font_color(self):
        return self._font_color

    @font_color.setter
    def font_color(self, value):
        self._font_color = value
        self.canvas.font_color = value
        self.canvas.render()

    def reset(self):
        self.canvas.reset()
        self.centers = {}
        self.selection = ''
        try:
            keyboard.unhook(self.keyboard_hook)
        except KeyError:
            pass

    def _on_key_press(self, on_done, key):
        x_key = not self.selection and key.name in self._xiterable
        y_key = self.selection and key.name in self._yiterable
        is_backspace = key.name == 'backspace'
        is_escape = key.name == 'esc'
        do_keypress = not (x_key or y_key or is_backspace or is_escape)
        if do_keypress:
            if key.event_type == 'down':
                keyboard.send(key.scan_code, do_press=True, do_release=False)
            else:
                keyboard.send(key.scan_code, do_press=False, do_release=True)
        elif key.event_type == 'up':
            if x_key:
                self.overlay(row=key.name, on_done=on_done, xiterable=self._xiterable, yiterable=self._yiterable)
                self.selection += key.name
            elif y_key:
                x, y = self.centers[f'{self.selection}{key.name}']
                mouse.move(x, y)
                if on_done is not None:
                    on_done()
                self.empty()                
            elif is_backspace:
                self.overlay(on_done=on_done)
            elif is_escape:
                self.empty()

    def overlay(self, row=None, on_done=None, xiterable=ALL_CHARS, yiterable=ALL_CHARS):
        self._xiterable, self._yiterable = xiterable, yiterable
        self.reset()
        self.keyboard_hook = keyboard.hook(functools.partial(self._on_key_press, on_done), suppress=True)
        xsize, xremainder = divmod(self.canvas.width, len(xiterable))
        ysize, yremainder = divmod(self.canvas.height, len(yiterable))  
        y = self.canvas.y
        for i, row_letter in enumerate(xiterable):
            x = self.canvas.x
            recheight = ysize
            if i < yremainder:
                recheight += 1
            if row is None or row == row_letter:    
                for j, col_letter in enumerate(yiterable):
                    recwidth = xsize
                    if j < xremainder:
                        recwidth += 1
                    self.centers[f'{row_letter}{col_letter}'] = x + recwidth//2, y + recheight//2
                    self.canvas.add_rectangle(x, y, recwidth, recheight, f'{row_letter}{col_letter}')
                    x += recwidth
            y += recheight
        self.canvas.render()

    def empty(self):
        self.reset()
        self.canvas.render()