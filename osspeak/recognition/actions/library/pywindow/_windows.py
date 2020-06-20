'''
Collection of Windows-specific I/O functions
'''

import msvcrt
import time
import ctypes
import weakref
from ctypes.wintypes import POINT, RECT
user32 = ctypes.windll.user32

SW_RESTORE = 9
SPIF_SENDCHANGE = 2
SPI_GETFOREGROUNDLOCKTIMEOUT = 0x2000
SPI_SETFOREGROUNDLOCKTIMEOUT = 0x2001
GW_OWNER = 4
GWL_EXSTYLE = -20
WS_EX_TOOLWINDOW = 128
WS_EX_APPWINDOW = 262144
WM_CLOSE = 0x0010
HWND_NOTOPMOST = -2
SWP_NOMOVE = 2
SWP_NOSIZE = 1
HWND_TOPMOST = 1
SWP_SHOWWINDOW = 64


hwnd_map = weakref.WeakKeyDictionary()

EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible

def flush_io_buffer():
    while msvcrt.kbhit():
        print(msvcrt.getch().decode('utf8'), end='')

def close_active_window():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.user32.PostMessageA(hwnd, WM_CLOSE, 0, 0)

def maximize_active_window():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.user32.ShowWindow(hwnd, 3)

def window_title(hwnd):
    length = GetWindowTextLength(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    return buff.value
    

class WindowImplementation:

    def __init__(self, hwnd):
        self.hwnd = hwnd

    @property
    def title(self):
        return window_title(self.hwnd)

    def maximize(self):
        ctypes.windll.user32.ShowWindow(self.hwnd, 3)

    def minimize(self):
        ctypes.windll.user32.ShowWindow(self.hwnd, 6)

    def close(self):
        ctypes.windll.user32.PostMessageA(self.hwnd, WM_CLOSE, 0, 0)
        
    @property
    def coords(self):
        r = RECT()
        user32.GetWindowRect(self.hwnd, ctypes.byref(r))
        x, y = r.left, r.top
        w = r.right - x
        h = r.bottom - y
        return x, y, w, h

    def focus(self):
        IsIconic = ctypes.windll.user32.IsIconic
        ShowWindow = ctypes.windll.user32.ShowWindow
        GetForegroundWindow = ctypes.windll.user32.GetForegroundWindow
        GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
        BringWindowToTop = ctypes.windll.user32.BringWindowToTop
        AttachThreadInput = ctypes.windll.user32.AttachThreadInput
        SetForegroundWindow = ctypes.windll.user32.SetForegroundWindow
        SystemParametersInfo = ctypes.windll.user32.SystemParametersInfoA
        
        if IsIconic(self.hwnd):
            ShowWindow(self.hwnd, SW_RESTORE)
        if GetForegroundWindow() == self.hwnd:
            return True
        ForegroundThreadID = GetWindowThreadProcessId(GetForegroundWindow(), None)
        ThisThreadID = GetWindowThreadProcessId(self.hwnd, None)
        if AttachThreadInput(ThisThreadID, ForegroundThreadID, True):
            BringWindowToTop(self.hwnd)
            SetForegroundWindow(self.hwnd)
            AttachThreadInput(ThisThreadID, ForegroundThreadID, False)
            if GetForegroundWindow() == self.hwnd:
                return True
        timeout = ctypes.c_int()
        zero = ctypes.c_int(0)
        SystemParametersInfo(SPI_GETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(timeout), 0)
        (SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(zero), SPIF_SENDCHANGE)
        BringWindowToTop(self.hwnd)
        SetForegroundWindow(self.hwnd)
        SystemParametersInfo(SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(timeout), SPIF_SENDCHANGE); 
        if GetForegroundWindow() == self.hwnd:
            return True
        return False

def is_real_window(hwnd):
    '''Return True iff given window is a real Windows application window.'''
    if not IsWindowVisible(hwnd):
        return False
    if user32.GetParent(hwnd) != 0:
        return False
    hasNoOwner = user32.GetWindow(hwnd, GW_OWNER) == 0
    lExStyle = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    if (((lExStyle & WS_EX_TOOLWINDOW) == 0 and hasNoOwner)
      or ((lExStyle & WS_EX_APPWINDOW != 0) and not hasNoOwner)):
        if window_title(hwnd):
            return True
    return False

def all_windows():
    windows = []

    def window_enum_callback(hwnd, _):
        if is_real_window(hwnd):
            window = create_application_window(hwnd)
            windows.append(window)
        return True

    EnumWindows(EnumWindowsProc(window_enum_callback), 0)
    return windows

def foreground_window():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    return create_application_window(hwnd)

def create_application_window(hwnd):
    from recognition.actions.library.pywindow.appwindow import ApplicationWindow
    impl = WindowImplementation(hwnd)
    return ApplicationWindow(impl)