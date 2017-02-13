from sprecgrammars.functions.library import mouse, window, keys, state, system, extensions, general, text, clipboard

builtin_functions = {
    'eval': general.python_evaluate,
    'hold': keys.hold,
    'length': text.length,
    'release': keys.release,
    'start': window.start,
    'shell': window.shell,

    'clipboard.get': clipboard.get,
    'clipboard.set': clipboard.set,

    'extensions.run': extensions.run,
    'extensions.message': extensions.send_message,

    'mouse.click': mouse.click,
    'mouse.move': mouse.move,
    'mouse.x': mouse.x,
    'mouse.y': mouse.y,

    'state.set': state.set_state,
    'state.delete': state.delete_state,
    'state.get': state.get_state,

    'window.focus': window.focus,
    'window.close': window.close,
    'window.maximizeActive': window.maximise_active,

    'wait': system.wait,
}