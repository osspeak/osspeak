import os
import sys

if sys.platform == 'win32':
    import recognition.actions.library.pywindow._windows as os_specific_implementation 
else:
    raise RuntimeError('Only Windows is currently supported.')

def all_windows():
    return os_specific_implementation.all_windows()

def foreground_window():
    return os_specific_implementation.foreground_window()

class WindowDoesNotExistError(BaseException):
    pass