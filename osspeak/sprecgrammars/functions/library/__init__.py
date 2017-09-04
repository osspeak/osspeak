from sprecgrammars.functions.library import (mouse, window, keys, state, system,
extensions, general, text, clipboard, osspeak, conditionals, history, fsystem, math)

builtin_functions = globals()

builtin_functions_custom_evaluation = set([
    'async',
    'if',
    'repeat'
])
