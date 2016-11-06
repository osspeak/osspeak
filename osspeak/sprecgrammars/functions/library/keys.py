from platforms import api
import time

def hold(keys):
    print('hold')
    api.type_keypresses(keys, direction='down')

def release(keys):
    print('release')
    api.type_keypresses(keys, direction='up')
    