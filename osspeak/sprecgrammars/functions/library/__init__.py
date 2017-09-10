from sprecgrammars.functions.library import (mouse, window, keys, state, system,
extensions, general, text, clipboard, osspeak, conditionals, history, fsystem, math)

builtin_functions = globals().copy()
from platforms import api
from sprecgrammars.functions.library import flow
import subprocess
import time
builtin_functions.update({
    'keys': keys.press,
    # 'keys': lambda *keys: api.type_keypresses(keys),
    'start': window.start,
    'wait': time.sleep,
    'repeat': flow.repeat,
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