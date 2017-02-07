from sprecgrammars.functions.library import mouse, window, keys, state, system, extensions, general

builtin_functions = {
    'hold': keys.hold,
    'release': keys.release,
    'start': window.start,
    'shell': window.shell,

    'eval': general.python_evaluate,

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

    'wait': system.wait,
}