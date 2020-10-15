# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

import ctypes
import time

HELD = set()

SendInput = ctypes.windll.user32.SendInput

mouse_button_down_mapping = {
    'left': 0x0002,
    'middle': 0x0020,
    'right': 0x0008
}

mouse_button_up_mapping = {
    'left': 0x0004,
    'middle': 0x0040,
    'right': 0x0010
}

CODES = {
    'esc': 0x01,
    'escape': 0x01,
    '1': 0x02,
    '2': 0x03,
    '3': 0x04,
    '4': 0x05,
    '5': 0x06,
    '6': 0x07,
    '7': 0x08,
    '8': 0x09,
    '9': 0x10,
    'q': 0x10,
    'w': 0x11,
    'e': 0x12,
    'r': 0x13,
    't': 0x14,
    'y': 0x15,
    'u': 0x16,
    'i': 0x17,
    'o': 0x18,
    'p': 0x19,
    'a': 0x1E,
    's': 0x1F,
    'd': 0x20,
    'f': 0x21,
    'g': 0x22,
    'h': 0x23,
    'j': 0x24,
    'k': 0x25,
    'l': 0x26,
    'z': 0x2C,
    'x': 0x2D,
    'c': 0x2E,
    'v': 0x2F,
    'b': 0x30,
    'n': 0x31,
    'm': 0x32,
    'ctrl': 0x1D,
    'pageup': 0xC9 + 1024,
    'pagedown': 0xD1 + 1024,
    'up': 0xC8,
    'left': 0xCB,
    'right': 0xCD,
    'down': 0xD0,
    'alt': 0x38,
}

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def release_all():
    held = list(HELD)
    for key in held:
        release(key)
        try:
            HELD.remove(key)
        except KeyError:
            pass

def hold(key):
    hexKeyCode = CODES[str(key)]
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    HELD.add(key)

def release(key):
    hexKeyCode = CODES[str(key)]
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    HELD.remove(key)

def send(keys):
    delay = .1
    for key in keys:
        hold(key)
        time.sleep(delay)
        release(key)
    # for code in keycodes:
    #     time.sleep(delay)

def click_down(button='left'):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, mouse_button_down_mapping[button], 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def click_up(button='left'):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, mouse_button_up_mapping[button], 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def click(button='left', duration=0.05):
    click_down(button=button)
    time.sleep(duration)
    click_up(button=button)

if __name__ == '__main__':
    time.sleep(10)
    click() 
    # send(['w'])
    # for i in range(100):
    #     send('wasd')
    #     hold(CODES['w'])
    #     time.sleep(5)
    #     release(CODES['w'])
    #     time.sleep(5)
        # hold(ONE)
        # release(ONE)
        # time.sleep(1)
        # hold(TWO)
        # time.sleep(1)
        # release(TWO)
        # time.sleep(1)