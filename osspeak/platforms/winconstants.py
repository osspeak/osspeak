import ctypes as ct

class POINT(ct.Structure):
    _fields_ = [("x", ct.c_ulong), ("y", ct.c_ulong)]

PUL = ct.POINTER(ct.c_ulong)
GMEM_DDESHARE = 0x2000
WM_CLOSE = 0x0010
ASFW_ANY = -1
HWND_TOPMOST = -1

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

SW_RESTORE = 9
SPIF_SENDCHANGE = 2
SPI_GETFOREGROUNDLOCKTIMEOUT = 0x2000
SPI_SETFOREGROUNDLOCKTIMEOUT = 0x2001

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004

WHEEL_DELTA = 120
XBUTTON1 = 0x0001
XBUTTON2 = 0x0002
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_HWHEEL = 0x01000
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_MOVE_NOCOALESCE = 0x2000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_VIRTUALDESK = 0x4000
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP = 0x0100

class KEYBOARD_INPUT(ct.Structure):
    _fields_ = [("wVk", ct.c_ushort),
                ("wScan", ct.c_ushort),
                ("dwFlags", ct.c_ulong),
                ("time", ct.c_ulong),
                ("dwExtraInfo", PUL)]

class HARDWARE_INPUT(ct.Structure):
    _fields_ = [("uMsg", ct.c_ulong),
                ("wParamL", ct.c_short),
                ("wParamH", ct.c_ushort)]

class MOUSE_INPUT(ct.Structure):
    _fields_ = [("dx", ct.c_long),
                ("dy", ct.c_long),
                ("mouseData", ct.c_ulong),
                ("dwFlags", ct.c_ulong),
                ("time",ct.c_ulong),
                ("dwExtraInfo", PUL)]

class INPUT_I(ct.Union):
    _fields_ = [("ki", KEYBOARD_INPUT),
                 ("mi", MOUSE_INPUT),
                 ("hi", HARDWARE_INPUT)]

class INPUT(ct.Structure):
    _fields_ = [("type", ct.c_ulong),
                ("ii", INPUT_I)]

WINDOWS_KEYCODES = {
    'lmouse': 0x01,
    'rmouse': 0x02,
    'cancel': 0x03,
    'mmouse': 0x04,
    'x1mouse': 0x05,
    'x2mouse': 0x06,
    'back': 0x08,
    'backspace': 0x08,
    'tab': 0x09,
    'clear': 0x0C,
    'enter': 0x0D,
    'return': 0x0D,
    '\n': 0x0D,
    '\r\n': 0x0D,
    'shift': 0x10,
    'ctrl': 0x11,
    'control': 0x11,
    'alt': 0x12,
    'caps': 0x14,
    'esc': 0x1B,
    'escape': 0x1B,
    ' ': 0x20,
    'pageup': 0x21,
    'page_up': 0x21,
    'pagedown': 0x22,
    'page_down': 0x22,
    'end': 0x23,
    'home': 0x24,
    'left': 0x25,
    'up': 0x26,
    'right': 0x27,
    'down': 0x28,
    'select': 0x29,
    'print': 0x2A,
    'execute': 0x2B,
    'print_screen': 0x2C,
    'insert': 0x2D,
    'del': 0x2E,
    'delete': 0x2E,
    'help': 0X2F,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    'lwindows': 0x5B,
    'rwindows': 0x5C,
    'apps': 0x5D,
    'sleep': 0x5F,
    'numpad0': 0x60,
    'numpad1': 0x61,
    'numpad2': 0x62,
    'numpad3': 0x63,
    'numpad4': 0x64,
    'numpad5': 0x65,
    'numpad6': 0x66,
    'numpad7': 0x67,
    'numpad8': 0x68,
    'numpad9': 0x69,
    'f1': 0x70,
    'f2': 0x71,
    'f3': 0x72,
    'f4': 0x73,
    'f5': 0x74,
    'f6': 0x75,
    'f7': 0x76,
    'f8': 0x77,
    'f9': 0x78,
    'f10': 0x79,
    'f11': 0x7A,
    'f12': 0x7B,
    'f13': 0x7C,
    'f14': 0x7D,
    'f15': 0x7E,
    'f16': 0x7F,
    'f17': 0x80,
    'f18': 0x81,
    'f19': 0x82,
    'f20': 0x83,
    'f21': 0x84,
    'f22': 0x85,
    'f23': 0x86,
    'f24': 0x87,
    'numlock': 0x90,
    'scroll': 0x91,
    'lshift': 0xA0,
    'rshift': 0xA1,
    'mute': 0xAD,
    'volume_up': 0xAE,
    'volume_down': 0xAF,
    '.': 0xBE,
    ',': 0xBC,
    ';': 0xBA,
    "'": 0xDE,
    '/': 0xBF,
    '`': 0xC0,
    '-': 0xBD,
    '=': 0xBB,
    '[': 0xDB,
    '\\': 0xDC,
    ']': 0xDD,

}

WINDOWS_SHIFT_MAP = {
    ')': '0',
    '!': '1',
    '@': '2',
    '#': '3',
    '$': '4',
    '%': '5',
    '^': '6',
    '&': '7',
    '*': '8',
    '(': '9',
    '<': ',',
    '>': '.',
    '?': '/',
    '"': "'",
    ':': ';',
    '{': '[',
    '}': ']',
    '|': '\\',
    '~': '`',
    '_': '-',
    '+': '=',
}
