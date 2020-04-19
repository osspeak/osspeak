'''
All of the arguments in these functions are wrapped in 
lambdas in recognition.asttransform.py to prevent early binding
'''

def loop(context, *args):
    from recognition.actions.astree import exhaust_generator
    count = args[-1].evaluate(context)
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 1
    eval_args = args[:-1]
    for i in range(count):
        for eval_arg in eval_args:
            yield from exhaust_generator(eval_arg.evaluate_lazy(context))

def osspeak_if(context, *args):
    from recognition.actions.astree import exhaust_generator
    assert 1 < len(args) < 4
    condition_evaluation = args[0].evaluate(context)
    if condition_evaluation:
        yield from exhaust_generator(args[1].evaluate_lazy(context))
    elif len(args) >= 3:
        yield from exhaust_generator(args[2].evaluate_lazy(context))

def between(context, main_code, intermediate_code, count_ast):
    from recognition.actions.astree import exhaust_generator
    try:
        count = int(count_ast.evaluate(context))
    except (TypeError, ValueError):
        count = 1
    if count < 1:
        return
    for i in range(count - 1):
        yield from exhaust_generator(main_code.evaluate_lazy(context))
        yield from exhaust_generator(intermediate_code.evaluate_lazy(context))
    yield from exhaust_generator(main_code.evaluate_lazy(context))


def osspeak_while(*args):
    action_args = args[1:]
    while args[0]():
        for arg in action_args:
            arg()

def wait_for(condition, timeout=None):
    import time
    start = time.clock()
    timeout = timeout if timeout is None else float(timeout())
    while not condition():
        time.sleep(.01)
        if timeout and time.clock() - start > timeout:
            break
    