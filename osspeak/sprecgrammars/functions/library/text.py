def length(value):
    return len(str(value))

def upper(s):
    return s.upper()

def lower(s):
    return s.lower()

def replace(s, old, new, count=None):
    return s.replace(old, new, count)

def split(s, sep=None):
    return s.split(sep=sep)

def join(iterable, sep=' '):
    return sep.join(iterable)

def contains(s, search_value):
    return search_value in s

def camel_case(s, sep=None):
    spl = s.split(sep) if isinstance(s, str) else s
    val = ''
    for i, word in enumerate(spl):
        word = word.lower() if i == 0 else word.title()
        val += word
    return val

def pascal_case(s, sep=None):
    spl = s.split(sep) if isinstance(s, str) else s
    return ''.join(w.title() for w in spl)