from sprecgrammars.functions.library import (mouse, window, keys, state, system,
extensions, general, text, clipboard, osspeak, conditionals, history, fsystem, math)

builtin_functions = globals().copy()
from platforms import api
import subprocess
builtin_functions.update({
    'keys': lambda x: api.type_keypresses([x]),
    'start': window.start
})

builtin_functions_custom_evaluation = set([
    'async',
    'if',
    'repeat'
])
