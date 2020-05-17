import os
import time
import re
import subprocess
import pywindow

def focus(title, index=None):
    title = title.lower()
    index = 1 if index is None else int(index)
    if index > 0:
        index -= 1
    windows = [(w, w.title.lower()) for w in pywindow.all_windows()]
    windows = [(w, win_title) for w, win_title in windows if title in win_title]
    windows.sort(key=lambda x: len(x[1]))
    windows[index][0].focus()

def close():
    pywindow.foreground_window().close()

def maximize_active():
    pywindow.foreground_window().maximize()

def minimize_active():
    pywindow.foreground_window().minimize()

def start(name):
    os.startfile(name)

def shell(text):
    subprocess.run(text.split(), shell=True)

def active_window_name():
    return pywindow.foreground_window().title

def wait(test_title, timeout=10, raise_on_timeout=True):
    timeout_at = time.time() + timeout
    while not test(test_title):
        now = time.time()
        if now > timeout_at:
            if raise_on_timeout:
                raise RuntimeError('window.wait timed out')
            return False
        time.sleep(0.1)
    return True

def external():
    pass

def test(s):
    title = active_window_name().lower()
    if isinstance(s, str):
        return s.lower() in title
    if isinstance(s, re.Pattern):
        return s.match(title, re.IGNORECASE)
    raise TypeError