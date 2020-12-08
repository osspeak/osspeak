import contextlib
from platforms.api import get_clipboard_contents, set_clipboard_contents

def get():
    return get_clipboard_contents()

def set(value):
    set_clipboard_contents(str(value))

@contextlib.contextmanager
def save_current():
    current = get()
    try:
        yield
    except Exception as e:
        raise e
    finally:
        set(current)
