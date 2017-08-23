import re

def variable_error(s, offset, match):
    matched_text = match.group()
    num = int(matched_text[1:])
    if num > 0:
        num -= 1
    pre = s[:offset]
    post = s[offset + len(matched_text):]
    new_text = f'{pre}variables[{num}]{post}'
    return greedy_parse(new_text)

variables = ['var1', 'var2']

error_map = {
    r'\$-?\d+': variable_error
}
error_map = {re.compile(k): v for k, v in error_map.items()}

def compile_python_expressions(input_string):
    expressions = []
    remaining_text = input_string
    while remaining_text:
        expr, expr_text, remaining_text = greedy_parse(remaining_text)
        expressions.append((expr, expr_text))
    return expressions

def greedy_parse(s, validator=lambda x: compile(x, filename='<ast>', mode='eval')):
    assert s
    expr = None
    first_error = None
    expr_text = None
    remaining_text = None
    try_parse_string = ''
    for char in s:
        try_parse_string += char
        try:
            expr = validator(try_parse_string)
            expr_text = try_parse_string
            remaining_text = s[len(expr_text):]
        except SyntaxError as e:
            handled_error = on_error(try_parse_string, e.offset - 1)
            if handled_error is None:
                first_error = first_error or e
            else:
                expr, expr_text, remaining_text = handled_error
    if expr is None:
        raise first_error
    return expr, expr_text, remaining_text

def on_error(s, offset):
    remainder = s[offset:]
    for pattern, handler in error_map.items():
        match = pattern.match(remainder)
        if match is not None:
            return handler(s, offset, match)

vals = [
    '"hello world"',
    '"hello" 42',
    '$1',
    '$1 0 or 7',
]

for val in vals:
    comp = compile_python_expressions(val)
    for exp in comp:
        print(eval(exp[0]))
    