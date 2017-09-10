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
    worker = recognition.results_map[threading.current_thread()]
    now = time.clock()
    if worker['last_keys'] is not None:
        diff = time.clock() - worker['last_keys']
        time.sleep(max(.05 - diff, 0))
    api.type_keypresses(keys)
    worker['last_keys'] = time.clock()
        