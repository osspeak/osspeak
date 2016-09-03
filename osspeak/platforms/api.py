# from osspeak import keyinput
from platforms import platformhandler

def send_string(string_to_send, delay=.02, direction='both'):
    tokenized_keys = keyinput.tokenize_keypresses(string_to_send)
    platformhandler.transcribe_line(tokenized_keys, delay, direction)

def mouse_move(x=None, y=None, relative=True):
    platformhandler.mouse_move(x, y, relative)

def mouse_click(button='left', direction='both', number=1):
    platformhandler.mouse_click(button, direction, number)

def activate_window(title):
	'''
	title is a string or list of strings
	'''
	platformhandler.activate_window(title)
    
def maximize_active_window():
    platformhandler.maximize_active_window()

def type_literal(text):
    platformhandler.type_literal(text)