import threading
import keyboard
from platforms import api
import time
import threading

shortcuts = {
    'back': 'backspace'
}

def add_keyboard_shortcuts(keys):
    new_keys = []
    for combo in keys:
        new_keys.append([shortcuts.get(k, k) for k in combo])
    return new_keys

def hold(keys):
    api.type_keypresses(keys, direction='down')

def press(keys):
    keyboard.press(add_keyboard_shortcuts(keys))

def release(keys):
    keyboard.release(add_keyboard_shortcuts(keys))

def press_and_release(keys):
    keyboard.send(add_keyboard_shortcuts(keys))