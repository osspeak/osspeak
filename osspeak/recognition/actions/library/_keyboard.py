import threading
from lib import keyboard
from recognition.actions.library.vocola import dragonkeys, sendinput
from platforms import api
import time
import threading

shortcuts = {
    'back': 'backspace'
}

class KeyDelayer:

    def __init__(self):
        self.delays_by_key = {}

key_delayer = KeyDelayer()


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
    specification = '{' + '+'.join(flattened_keys) + '}'
    key_events = dragonkeys.senddragonkeys_to_events(specification)
    sendinput.send_input(key_events)

def write(text, delay=.05):
    events = []
    for char in text:
        events.extend(dragonkeys.chord_to_events([None, char, None, char]))
    sendinput.send_input(events)