def loop(context, *args):
    from recognition.actions.astree import exhaust_generator, KeySequence
    count = args[-1].evaluate(context)
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 1
    eval_arg = args[0]
    # merge consecutive keypresses
    if isinstance(eval_arg, KeySequence):
        kp = eval_arg.evaluate(context)
        assert len(kp.chords) == 1
        press_count = kp.chords[0][2]
        if press_count is None:
            press_count = 1
        press_count = str(count * int(press_count))
        kp.chords[0][2] = press_count
        yield eval_arg, kp
    else:
        for i in range(count):
            yield from exhaust_generator(eval_arg.evaluate_lazy(context))

def osspeak_if(context, test_condition, then_node, else_node=None):
    from recognition.actions.astree import exhaust_generator
    if test_condition.evaluate(context):
        yield from exhaust_generator(then_node.evaluate_lazy(context))
    elif else_node is not None:
        yield from exhaust_generator(else_node.evaluate_lazy(context))

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

def osspeak_while(context, test_condition, *args):
    while test_condition.evaluate(context):
        for arg in args:
            yield from exhaust_generator(arg.evaluate_lazy(context))

def wait_for(condition, timeout=None):
    import time
    start = time.clock()
    timeout = timeout if timeout is None else float(timeout())
    while not condition():
        time.sleep(.01)
        if timeout and time.clock() - start > timeout:
            break
    