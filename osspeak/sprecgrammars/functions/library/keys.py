import threading
from platforms import api
import time
import threading

def hold(keys):
    api.type_keypresses(keys, direction='down')

def release(keys):
    api.type_keypresses(keys, direction='up')
    
def press(*keys):
    from client import recognition
    with recognition.keypress_delay():
        api.type_keypresses(keys)