from platforms import api

def click():
    api.mouse_click()

def move():
    print('asdasda')

def x():
    return api.get_mouse_location()[0]

def y():
    return api.get_mouse_location()[1]