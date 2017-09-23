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
            import time
            # time.sleep(3)