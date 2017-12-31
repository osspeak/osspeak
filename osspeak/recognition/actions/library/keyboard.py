import threading
import keyboard
from platforms import api
import time
import threading

def hold(keys):
    api.type_keypresses(keys, direction='down')

def press(keys):
    keyboard.press(keys)

def release(keys):
    keyboard.release(keys)

def press_and_release(keys):
    keyboard.send(keys)