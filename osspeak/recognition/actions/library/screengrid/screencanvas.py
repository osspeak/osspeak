import win32api, win32con, win32gui, win32ui
import ctypes
from typing import List
import threading
import time
import string
import uuid
import ctypes
import queue
from . import rectangle, win32_contants

def draw_loop(_queue: queue.Queue):
    while True:
        try:
            canvas = _queue.get(block=True, timeout=0.02)
        except queue.Empty:
            pass
        else:
            canvas.initial_draw()
        finally:
            win32gui.PumpWaitingMessages()

draw_queue = queue.Queue()
draw_thread = threading.Thread(target=draw_loop, args=(draw_queue,), daemon=True)
draw_thread.start()

class ScreenCanvas:         

    def __init__(
        self,
        x = 0,
        y = 0,
        width = ctypes.windll.user32.GetSystemMetrics(win32_contants.SM_CXSCREEN),
        height = ctypes.windll.user32.GetSystemMetrics(win32_contants.SM_CYSCREEN),
        font_color = (0, 0, 0)
    ):
        self.window_handle = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_color = font_color
        self.rectangles: List[rectangle.Rectangle] = []
        self._wndClassAtom, self._hInstance = self._win32_setup()
        self.window_rendered = threading.Event()
        self.render_lock = threading.Lock()

    def add_rectangle(self, x: int, y: int, width: int, height: int, text=None):
        rect = rectangle.Rectangle(x, y, width, height, text=text)
        self.rectangles.append(rect)

    def reset(self):
        self.rectangles = []

    def render(self):
        with self.render_lock:
            if self.window_handle is None:
                self.window_handle = 'placeholder'
                draw_queue.put(self)
            else:
                self.window_rendered.wait()
                win32gui.RedrawWindow(self.window_handle, None, None, win32_contants.RDW_INVALIDATE | win32_contants.RDW_ERASE)

    def initial_draw(self):
        self.window_handle = win32gui.CreateWindowEx(
            win32_contants.EX_STYLE,
            self._wndClassAtom,
            None, # WindowName
            win32_contants.STYLE,
            self.x,
            self.y,
            self.width,
            self.height,
            None, # hWndParent
            None, # hMenu
            self._hInstance,
            None # lpParam
        )
            # http://msdn.microsoft.com/en-us/library/windows/desktop/ms633540(v=vs.85).aspx
        win32gui.SetLayeredWindowAttributes(self.window_handle, 0x00ffffff, 255, win32_contants.LWA_COLORKEY | win32_contants.LWA_ALPHA)

        # http://msdn.microsoft.com/en-us/library/windows/desktop/dd145167(v=vs.85).aspx
        #win32gui.UpdateWindow(self.window_handle)
        # http://msdn.microsoft.com/en-us/library/windows/desktop/ms633545(v=vs.85).aspx
        win32gui.SetWindowPos(self.window_handle, win32_contants.HWND_TOPMOST, 0, 0, 0, 0,
            win32_contants.SWP_NOACTIVATE | win32_contants.SWP_NOMOVE | win32_contants.SWP_NOSIZE | win32_contants.SWP_SHOWWINDOW)
        self.window_rendered.set()

    def _win_message(self, hWnd, message, wParam, lParam):
        if message == win32_contants.WM_PAINT:
            device_context_handle, paintStruct = win32gui.BeginPaint(hWnd)
            dpiScale = ctypes.windll.gdi32.GetDeviceCaps(device_context_handle, win32_contants.LOGPIXELSX) / 60.0
            fontSize = 14

            # http://msdn.microsoft.com/en-us/library/windows/desktop/dd145037(v=vs.85).aspx
            lf = win32gui.LOGFONT()
            lf.lfFaceName = "Times New Roman"
            # lf.lfHeight = int(round(dpiScale * fontSize))
            lf.lfHeight = 20
            lf.lfWeight = 0
            # Use nonantialiased to remove the white edges around the text.
            lf.lfQuality = win32con.NONANTIALIASED_QUALITY
            hf = win32gui.CreateFontIndirect(lf)
            win32gui.SetTextColor(device_context_handle, win32_color(self.font_color))
            win32gui.SelectObject(device_context_handle, hf)
            self._draw(device_context_handle)
            win32gui.EndPaint(hWnd, paintStruct)
            return 0
        elif message == win32_contants.WM_DESTROY:
            win32gui.PostQuitMessage(0)
            return 0
        else:
            return win32gui.DefWindowProc(hWnd, message, wParam, lParam)

    def _draw(self, device_context_handle):
        for rect in self.rectangles:
            rect.draw(device_context_handle)

    def _win32_setup(self):
        hInstance = win32api.GetModuleHandle()
        className = str(uuid.uuid4()) # probably a better way to do this

        # http://msdn.microsoft.com/en-us/library/windows/desktop/ms633576(v=vs.85).aspx
        # win32gui does not support WNDCLASSEX.
        wndClass                = win32gui.WNDCLASS()
        # http://msdn.microsoft.com/en-us/library/windows/desktop/ff729176(v=vs.85).aspx
        wndClass.style          = win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wndClass.lpfnWndProc    = self._win_message
        wndClass.hInstance      = hInstance
        wndClass.hCursor        = win32gui.LoadCursor(None, win32con.IDC_ARROW)
        wndClass.hbrBackground  = win32gui.GetStockObject(win32con.WHITE_BRUSH)
        wndClass.lpszClassName  = className
        # win32gui does not support RegisterClassEx
        wndClassAtom = win32gui.RegisterClass(wndClass)
        return wndClassAtom, hInstance

def win32_color(color):
    if isinstance(color, (tuple, list)):
        return win32api.RGB(*color)