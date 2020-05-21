'''
Collection of Windows-specific I/O functions
'''

import msvcrt
import time
import ctypes
from platforms import winconstants, winclipboard

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
    ctypes.windll.user32.PostMessageA(hwnd, winconstants.WM_CLOSE, 0, 0)

def get_active_window_name():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    return get_window_title(hwnd)
    
def maximize_active_window():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.user32.ShowWindow(hwnd, 3)

def minimize_active_window():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    ctypes.windll.user32.ShowWindow(hwnd, 6)

def get_window_title(hwnd):
    length = GetWindowTextLength(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    GetWindowText(hwnd, buff, length + 1)
    return buff.value

def get_matching_windows(title_list):
    matches = {}

    def window_enum_callback(hwnd, lParam):
        if IsWindowVisible(hwnd):
            window_name = get_window_title(hwnd).lower()
            for name in title_list:
                if name not in window_name:
                    return True
            matches[window_name] = hwnd
        return True

    EnumWindows(EnumWindowsProc(window_enum_callback), 0)
    return matches

def activate_window(title, position=1):
    if position > 0:
        position -= 1
    matches = get_matching_windows(title)
    sorted_keys = list(sorted(matches.keys(), key=len))
    key = sorted_keys[position]
    hwnd = matches[key]
    # magic incantations to activate window consistently
    IsIconic = ctypes.windll.user32.IsIconic
    ShowWindow = ctypes.windll.user32.ShowWindow
    GetForegroundWindow = ctypes.windll.user32.GetForegroundWindow
    GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
    BringWindowToTop = ctypes.windll.user32.BringWindowToTop
    AttachThreadInput = ctypes.windll.user32.AttachThreadInput
    SetForegroundWindow = ctypes.windll.user32.SetForegroundWindow
    SystemParametersInfo = ctypes.windll.user32.SystemParametersInfoA
    
    if IsIconic(hwnd):
        ShowWindow(hwnd, winconstants.SW_RESTORE)
    if GetForegroundWindow() == hwnd:
        return True
    ForegroundThreadID = GetWindowThreadProcessId(GetForegroundWindow(), None)
    ThisThreadID = GetWindowThreadProcessId(hwnd, None)
    if AttachThreadInput(ThisThreadID, ForegroundThreadID, True):
        BringWindowToTop(hwnd)
        SetForegroundWindow(hwnd)
        AttachThreadInput(ThisThreadID, ForegroundThreadID, False)
        if GetForegroundWindow() == hwnd:
            return True
    timeout = ctypes.c_int()
    zero = ctypes.c_int(0)
    SystemParametersInfo(winconstants.SPI_GETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(timeout), 0)
    (winconstants.SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(zero), winconstants.SPIF_SENDCHANGE)
    BringWindowToTop(hwnd)
    SetForegroundWindow(hwnd)
    SystemParametersInfo(winconstants.SPI_SETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(timeout), winconstants.SPIF_SENDCHANGE); 
    if GetForegroundWindow() == hwnd:
        return True
    return False

def get_mouse_location():
    pt = winconstants.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def mouse_click(button, direction, number):
    event_nums = get_mouse_event_nums(button, direction)
    for i in range(number):
        for num in event_nums:
            ctypes.windll.user32.mouse_event(num, 0, 0, 0, 0)

def mouse_move(x=None, y=None, relative=False):
    startx, starty = get_mouse_location()
    if not relative:
        if x is None: x = startx
        if y is None: y = starty
        ctypes.windll.user32.SetCursorPos(x, y)
        return
    if x is None: x = 0
    if y is None: y = 0
    ctypes.windll.user32.SetCursorPos(startx + x, starty + y)

def get_clipboard_contents():
    return winclipboard.init_windows_clipboard()[1]()

def set_clipboard_contents(text):
    return winclipboard.init_windows_clipboard()[0](str(text))

def get_mouse_event_nums(button, direction):
    if button == 'left' and direction == 'down': return [2]
    if button == 'left' and direction == 'up': return [4]
    if button == 'left' and direction == 'both': return [2, 4]
    if button == 'right' and direction == 'down': return [8]
    if button == 'right' and direction == 'up': return [16]
    if button == 'right' and direction == 'both': return [8, 16]