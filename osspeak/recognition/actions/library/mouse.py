from platforms import api

def click():
    api.mouse_click()

def move(x=None, y=None, relative=False):
    currentx, currenty = api.get_mouse_location()
    x = currentx if x is None else x
    y = currenty if y is None else y
    api.mouse_move(int(x), int(y), relative)

def x():
    return api.get_mouse_location()[0]

def y():
    return api.get_mouse_location()[1]
