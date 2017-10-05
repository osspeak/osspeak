from platforms.api import get_clipboard_contents, set_clipboard_contents

def get():
    return get_clipboard_contents()

def set(value):
    set_clipboard_contents(str(value))