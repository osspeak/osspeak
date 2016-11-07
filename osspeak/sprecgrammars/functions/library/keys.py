from platforms import api
import time

def hold(keys):
    api.type_keypresses(keys, direction='down')

def release(keys):
    api.type_keypresses(keys, direction='up')
    