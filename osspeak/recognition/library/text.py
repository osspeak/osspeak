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

def snake_case(s):
    return case(s, '_')

def case(s, delim):
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', rf'\1{delim}\2', s)
    s2 = re.sub('([a-z0-9])([A-Z])', rf'\1{delim}\2', s1).lower()
    return re.sub(r'\{delim}+', delim, s2)