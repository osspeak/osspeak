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

# def release(keys):
#     api.type_keypresses(keys, direction='up')
    
def send_and_release(*keys):
    from recognition.actions import perform
    perform.keyboard_event('keys', keys, api.type_keypresses)