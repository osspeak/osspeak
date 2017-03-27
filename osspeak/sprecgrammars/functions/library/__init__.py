from sprecgrammars.functions.library import (mouse, window, keys, state, system,
extensions, general, text, clipboard, osspeak, conditionals, history)

builtin_functions = {
    'eval': general.python_evaluate,
    'list': general.python_list,
    'hold': keys.hold,
    'print': general.python_print,
    'release': keys.release,
    'start': window.start,
    'shell': window.shell,

    'clipboard.get': clipboard.get,
    'clipboard.set': clipboard.set,

    'if': conditionals.osspeak_if,
    'repeat': conditionals.repeat,

    'extensions.call': extensions.call,
    'extensions.message': extensions.send_message,
    'extensions.run': extensions.run,

    'history.last': history.last,

    'mouse.click': mouse.click,
    'mouse.move': mouse.move,
    'mouse.x': mouse.x,
    'mouse.y': mouse.y,

    'osspeak.reload': osspeak.reload,

    'state.set': state.set_state,
    'state.delete': state.delete_state,
    'state.get': state.get_state,

    'text.contains': text.contains,
    'text.join': text.join,
    'text.length': text.length,
    'text.lower': text.lower,
    'text.replace': text.replace,
    'text.split': text.split,
    'text.upper': text.upper,

    'window.close': window.close,
    'window.focus': window.focus,
    'window.maximizeActive': window.maximise_active,
    'window.title': window.get_active_window_name,

    'wait': system.wait,
}

builtin_functions_custom_evaluation = set([
    'if',
    'repeat'
])