from sprecgrammars.functions.library import (mouse, window, keys, state,
extensions, general, text, clipboard, osspeak, conditionals, history, fsystem, math)

builtin_functions = globals().copy()
from platforms import api
from sprecgrammars.functions.library import flow
import subprocess
import time
from sprecgrammars.functions.library import system
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