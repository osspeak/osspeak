from recognition.actions.library import (window, thread,
extensions, general, text, clipboard, osspeak, conditionals, history,
fsystem, math, directinput, flow, process)
from recognition.actions.library import _mouse as mouse
from recognition.actions.library import _keyboard as keyboard
from types import SimpleNamespace
import operator
import screengrid
import time

def wait(n):
    time.sleep(n)

namespace = {
    'click': mouse.click,
    'eq': operator.eq,
    'eval': lambda context, x: eval(str(x.evaluate(context)), {}, context.namespace),
    'gt': operator.gt,
    'if': flow.osspeak_if,
    'index': lambda obj, key: obj[key],
    'int': int,
    'keypress': lambda *k: keyboard.press_and_release(list(k)),
    'lt': operator.lt,
    'loop': flow.loop,
    'mod': operator.mod,
    'mul': operator.mul,
    'print': print,
    'run': process.run,
    'run_sync': process.run_sync,
    'screengrid': screengrid,
    'state': SimpleNamespace(),
    'sub': operator.sub,
    'true': lambda: True,
    'wait': wait,
    'window': window,
}
namespace['setState'] = lambda name, value: setattr(namespace['state'], name, value)

deferred_arguments_eval = set([
    flow.osspeak_if,
    flow.loop,
    namespace['eval'],
])