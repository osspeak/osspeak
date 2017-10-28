'''
All of the arguments in these functions are wrapped in 
lambdas in recognition.asttransform.py to prevent early binding
'''

def repeat(*args):
    from recognition.actions import perform
    count = args[-1]()
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 1
    lambda_args = args[:-1]
    for i in range(count):
        for lambda_arg in lambda_args:
            perform.perform_io(lambda_arg())

def osspeak_if(*args):
    assert 1 < len(args) < 4
    condition_evaluation = args[0]()
    if condition_evaluation:
        return args[1]()
    if len(args) == 3:
        return args[2]()

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
    