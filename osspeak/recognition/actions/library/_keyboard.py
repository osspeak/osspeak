import threading
import keyboard
from platforms import api
import time
import threading

shortcuts = {
    'back': 'backspace'
}

def add_keyboard_shortcuts(keys):
    return [shortcuts.get(k, k) for k in keys]
    for item in keys:
        new_keys.append([shortcuts.get(k, k) for k in item])
    return new_keys

def hold(keys):
    api.type_keypresses(keys, direction='down')

def press(keys):
    keyboard.press(add_keyboard_shortcuts(keys))

def release(keys):
    keyboard.release(add_keyboard_shortcuts(keys))

def press_and_release(keys):
    new_keys = add_keyboard_shortcuts(keys)
    keyboard.press_and_release(new_keys)