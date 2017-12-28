from platforms import api
import mouse

def click():
    api.mouse_click()

def move(x=None, y=None, absolute=True, duration=0):
    mouse.move(x, y, absolute, duration)

def x():
    return api.get_mouse_location()[0]

def y():
    return api.get_mouse_location()[1]
