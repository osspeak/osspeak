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