from recognition.actions.library import (window, thread,
extensions, general, text, clipboard, osspeak, conditionals, history,
fsystem, math, directinput, flow)
from recognition.actions.library import _mouse as mouse
from recognition.actions.library import _keyboard as keyboard
from types import SimpleNamespace
import screengrid
import time

def wait(n):
    time.sleep(n)

namespace = {
    'click': mouse.click,
    'if': flow.osspeak_if,
    'keypress': lambda *k: keyboard.press_and_release(list(k)),
    'loop': flow.loop,
    'print': print,
    'state': SimpleNamespace(),
    'wait': wait,
    'window': window,
}
namespace['setState'] = lambda name, value: setattr(namespace['state'], name, value)

deferred_arguments_eval = set([
    flow.osspeak_if,
    flow.loop,
])