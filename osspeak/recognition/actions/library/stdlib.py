from recognition.actions.library import (window, thread, engines,
extensions, general, text, clipboard, macro, osspeak, conditionals,
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
        time.sleep(float(n))
    except TypeError:
        pass

def initialize():
    # avoid circular import timing issue
    macro._restore_saved()

namespace = {
    'active_window': lambda: window.active_window_name().title(),
    'between': flow.between,
    'camel_case': text.camel_case,
    'click': mouse.click,
    'dict': dict,
    'directinput': directinput,
    'engines': engines,
    'error': general.error,
    'eval': lambda context, x: eval(str(x.evaluate(context)), {}, context.namespace),
    'extensions': extensions,
    'false': lambda: False,
    'if': flow.osspeak_if,
    'int': int,
    'in': lambda a, b: a in b,
    'is': lambda a, b: a is b,
    'keyboard': keyboard,
    'len': len,
    'loop': flow.loop,
    'macro': macro,
    'mouse': mouse,
    'none': lambda: None,
    'print': print,
    'process': process,
    're': re,
    'read': fsystem.read_file,
    'run': process.run,
    'run_sync': process.run_sync,
    'screengrid': screengrid,
    'set': set,
    'setattr': setattr,
    'setState': lambda name, value: setattr(namespace['state'], name, value),
    'snake_case': text.snake_case,
    'state': SimpleNamespace(),
    'str': str,
    'text': text,
    'title_case': text.title_case,
    'true': lambda: True,
    'wait': wait,
    'window': window,
}

deferred_arguments_eval = set([
    flow.osspeak_if,
    flow.loop,
    flow.between,
    keyboard.add_delay,
    keyboard.remove_delay,
    namespace['eval'],
])