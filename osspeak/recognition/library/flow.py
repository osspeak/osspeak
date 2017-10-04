def repeat(*args):
    from recognition import perform
    count = args[-1]()
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 1
    largs = args[:-1]
    for i in range(count):
        for larg in largs:
            perform.perform_io(larg())

def osspeak_if(*args):
    assert 1 < len(args) < 4
    condition_evaluation = args[0]()
    if condition_evaluation:
        return args[1]()
    elif len(args) == 3:
        return args[2]()

def wait_for(condition, timeout=None):
    import time
    start = time.clock()
    timeout = timeout if timeout is None else float(timeout())
    while not condition():
        time.sleep(.01)
        if timeout and time.clock() - start > timeout:
            break
    