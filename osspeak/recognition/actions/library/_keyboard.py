import threading
from lib import keyboard
from recognition.actions.library.vocola.vocolakeys import send_input
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
    flattened_keys = []
    for s in keys:
        flattened_keys.extend(s.split(' '))
    send_input('{' + '+'.join(flattened_keys) + '}')