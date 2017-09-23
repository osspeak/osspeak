import threading

_STATE_LOCK = threading.Lock()
USER_DEFINED_STATE = {}

def set(key, val):
    with _STATE_LOCK:
        USER_DEFINED_STATE[key] = val

def delete(key):
    with _STATE_LOCK:
        del USER_DEFINED_STATE[key]

def get(key, default=None):
    with _STATE_LOCK:
        return USER_DEFINED_STATE.get(key, default)

def state_copy():
    with _STATE_LOCK:
        return USER_DEFINED_STATE.copy()

