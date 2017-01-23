USER_DEFINED_STATE = {}

def set_state(key, val):
    USER_DEFINED_STATE[key] = val

def delete_state(key):
    del USER_DEFINED_STATE[key]