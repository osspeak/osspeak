from sprecgrammars.functions.library import (mouse, window, keys, state, system,
extensions, general, text, clipboard, osspeak, conditionals, history, fsystem, math)

builtin_functions = globals().copy()
from platforms import api
import subprocess
import time
builtin_functions.update({
    'keys': lambda *keys: api.type_keypresses(keys),
    'start': window.start,
    'wait': time.sleep
})

builtin_functions_custom_evaluation = set([
    'async',
    'if',
    'repeat'
])
