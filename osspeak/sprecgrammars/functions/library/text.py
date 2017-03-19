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