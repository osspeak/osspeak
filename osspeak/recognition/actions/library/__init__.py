from recognition.actions.library import (mouse, window, keyboard, state, thread,
extensions, general, text, clipboard, osspeak, conditionals, history, fsystem, math)

builtin_functions = globals().copy()
from platforms import api
from recognition.actions.library import flow
import subprocess
import time
from recognition.actions.library import system
builtin_functions.update({
    'keys': keyboard.press_and_release,
    'start': window.start,
    'wait': time.sleep,
    'repeat': flow.repeat,
    'wait_for': flow.wait_for,
    'proc': system.proc,
    'path': system.path,
    'thread': thread.run_in_thread
})

lambda_arguments = set([tuple(x.split('.')) for x in [
    'repeat',
    'if',
    'wait_for',
    'while',
    'thread',
]])

builtins = __builtins__ if isinstance(__builtins__, dict) else dir(__builtins__)
namespace = {**builtin_functions, **builtins}