from sprecgrammars.functions.library import mouse, window, keys

builtin_functions = {
    'hold': keys.hold,
    'release': keys.release,
    'start': window.start,

    'mouse.click': mouse.click,

    'window.focus': window.focus,
    'window.close': window.close,
}