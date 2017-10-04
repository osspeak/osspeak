from recognition.library import (mouse, window, keys, state,
extensions, general, text, clipboard, osspeak, conditionals, history, fsystem, math)

builtin_functions = globals().copy()
from platforms import api
from recognition.library import flow
import subprocess
import time
from recognition.library import system
builtin_functions.update({
    'keys': keys.press,
    'start': window.start,
    'wait': time.sleep,
    'repeat': flow.repeat,
    'wait_for': flow.wait_for,
    'proc': system.proc,
    'path': system.path,
})

lambda_arguments = set([tuple(x.split('.')) for x in [
    'repeat',
    'if',
    'wait_for',
    'while',
]])

builtins = __builtins__ if isinstance(__builtins__, dict) else dir(__builtins__)
namespace = {**builtin_functions, **builtins}