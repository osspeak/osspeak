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
        # return args[1].evaluate_lazy(context)
    if len(args) == 4:
        yield from exhaust_generator(args[2].evaluate_lazy(context))
        # return args[2].evaluate(context)

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
    