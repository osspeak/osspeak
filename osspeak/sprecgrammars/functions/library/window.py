import os

from platforms import api

def focus(title, result_number=None):
    if not result_number:
        result_number = 1
    api.activate_window(title, int(result_number))

def close():
    api.close_active_window()

def maximise_active():
    api.maximize_active_window()

def start(name):
    os.startfile(name)

def shell(text):
    return os.system(text)

def get_active_window_name():
    return api.get_active_window_name()