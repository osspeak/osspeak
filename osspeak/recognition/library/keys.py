import threading
from platforms import api
import time
import threading

def hold(keys):
    api.type_keypresses(keys, direction='down')

def release(keys):
    api.type_keypresses(keys, direction='up')
    
def press(*keys):
    from recognition import perform
    with perform.keypress_delay():
        api.type_keypresses(keys)