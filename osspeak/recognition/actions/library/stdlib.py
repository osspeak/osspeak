from recognition.actions.library import (window, thread,
extensions, general, text, clipboard, osspeak, conditionals, history,
fsystem, math, directinput, flow, process)
from recognition.actions.library import _mouse as mouse
from recognition.actions.library import _keyboard as keyboard
from types import SimpleNamespace
import operator
import screengrid
import re
import time

def wait(n):
    try:
        count = float(n)
    except TypeError:
        count = 0
    time.sleep(count)

namespace = {
    'active_window': lambda: window.active_window_name().title(),
    'between': flow.between,
    'click': mouse.click,
    'directinput': directinput,
    'eval': lambda context, x: eval(str(x.evaluate(context)), {}, context.namespace),
    'false': lambda: False,
    'if': flow.osspeak_if,
    'index': lambda obj, key: obj[key],
    'int': int,
    'keyboard': keyboard,
    'loop': flow.loop,
    'mouse': mouse,
    'none': lambda: None,
    'print': print,
    're': re,
    'read': fsystem.read_file,
    'run': process.run,
    'run_sync': process.run_sync,
    'screengrid': screengrid,
    'state': SimpleNamespace(),
    'str': str,
    'true': lambda: True,
    'wait': wait,
    'window': window,
}
namespace['setState'] = lambda name, value: setattr(namespace['state'], name, value)

deferred_arguments_eval = set([
    flow.osspeak_if,
    flow.loop,
    flow.between,
    keyboard.add_delay,
    namespace['eval'],
])