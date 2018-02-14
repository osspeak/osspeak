import mouse

def click():
    mouse.click()

def move(x=None, y=None, absolute=True, duration=0):
    mouse.move(x, y, absolute, duration)

def x():
    return mouse.get_position()[0]

def y():
    return mouse.get_position()[1]