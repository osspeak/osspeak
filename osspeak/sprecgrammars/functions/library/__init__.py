from sprecgrammars.functions.library import mouse, window, keys, system

builtin_functions = {
    'hold': keys.hold,
    'release': keys.release,
    'start': window.start,

    'mouse.click': mouse.click,
    'mouse.move': mouse.move,
    'mouse.x': mouse.x,
    'mouse.y': mouse.y,

    'window.focus': window.focus,
    'window.close': window.close,

    'wait': system.wait,
}