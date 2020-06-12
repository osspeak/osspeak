import mouse

def click(button=mouse.LEFT):
    mouse.click(button=button)

def press(button=mouse.LEFT):
    mouse.press(button=button)

def release(button=mouse.LEFT):
    mouse.release(button=button)

def double_click(button=mouse.LEFT):
    mouse.double_click(button=button)

def right_click():
    mouse.right_click()

def move(x=None, y=None, absolute=True, duration=0):
    mouse.move(x, y, absolute, duration)

def move_relative(x=None, y=None, duration=0):
    move(x=x, y=y, absolute=False, duration=duration)

def move_absolute(x=None, y=None, duration=0):
    move(x=x, y=y, absolute=True, duration=duration)

def x():
    return mouse.get_position()[0]

def y():
    return mouse.get_position()[1]

def position():
    return mouse.get_position()

def wheel(delta=1):
    mouse.wheel(delta)

def drag(start_x, start_y, end_x, end_y, absolute=True, duration=0):
    mouse.drag(start_x, start_y, end_x, end_y, absolute=absolute, duration=duration)
    
def is_pressed(button=mouse.LEFT):
    return mouse.is_pressed(button=button)