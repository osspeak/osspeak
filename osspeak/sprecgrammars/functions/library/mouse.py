from platforms import api

def click():
    api.mouse_click()

def move(x=None, y=None):
    currentx, currenty = api.get_mouse_location()
    x = currentx if x is None else int(x)
    y = currenty if y is None else int(y)
    api.mouse_move(x, y, False)

def x():
    return api.get_mouse_location()[0]

def y():
    return api.get_mouse_location()[1]