def python_evaluate(text):
    return eval(str(text))

def python_print(*values, sep=' '):
    joined = sep.join((str(v) for v in values))
    print(joined)

def python_list(*args):
    return args

def error(text=''):
    raise RuntimeError(text)