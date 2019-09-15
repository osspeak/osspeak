from recognition.actions.library import (window, state, thread,
extensions, general, text, clipboard, osspeak, conditionals, history,
fsystem, math, directinput, flow)
from recognition.actions.library import _mouse as mouse
from recognition.actions.library import _keyboard as keyboard
import screengrid
import time

def wait(n):
    time.sleep(n)

namespace = {
    'keypress': lambda *k: keyboard.press_and_release(list(k)),
    'window': window,
    'if': flow.osspeak_if,
    'loop': flow.loop,
    'wait': wait
}

deferred_arguments_eval = set([
    flow.osspeak_if,
    flow.loop,
])