from recognition.actions.library import (window, thread, engine,
extensions, general, text, clipboard, macro, osspeak, conditionals,
fsystem, math, directinput, flow, process)
from recognition.actions.library import _mouse as mouse
from recognition.actions.library import _keyboard as keyboard
from recognition.actions.library import screengrid
from types import SimpleNamespace
import operator
import re
import time

def wait(n):
    try:
        time.sleep(float(n))
    except TypeError:
        pass

def assign_var(context, name, value):
    context.argument_frames[-1][name.evaluate(context)] = value.evaluate(context)


class _Nil:
    pass

def not_none(val, default):
    if val is not None:
        return val
    return default

def parse_int(val, default=1):
    if isinstance(val, str):
        val = val.replace(' ', '')
    try:
        return int(val)
    except (ValueError, TypeError) as e:
        return default
def initialize():
    # avoid circular import timing issue
    macro._restore_saved()

namespace = {
    'active_window': lambda: window.active_window_name().title(),
    'between': flow.between,
    'camel_case': text.camel_case,
    'click': mouse.click,
    'clipboard': clipboard,
    'dict': dict,
    'directinput': directinput,
    'engine': engine,
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
    'not_none': not_none,
    'parse_int': parse_int,
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
    'pascal_case': text.pascal_case,
    'true': lambda: True,
    'var': assign_var,
    'wait': wait,
    'while': flow.osspeak_while,
    'window': window,
}

deferred_arguments_eval = {
    flow.osspeak_if: flow.osspeak_if_gen,
    flow.osspeak_while: flow.osspeak_while_gen,
    flow.loop: flow.loop_gen,
    flow.between: None,
    keyboard.add_delay: None,
    keyboard.remove_delay: None,
    namespace['eval']: None,
    assign_var: None,
}