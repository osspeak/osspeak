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
    'proc': system.proc,
    'path': system.path,
})

builtin_functions_custom_evaluation = set([
    'async',
    'if',
    'repeat'
])

lambda_arguments = set([tuple(x.split('.')) for x in [
    'repeat',
    'flow.while',
]])

builtins = __builtins__ if isinstance(__builtins__, dict) else dir(__builtins__)
namespace = {**builtin_functions, **builtins}