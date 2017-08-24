import re

def varrepl(matched_text):
    num = int(matched_text[1:])
    if num > 0:
        num -= 1
    return f'variables[{num}]'

VAR_PATTERN = re.compile(r'\$-?\d+')

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
    expr_matches = None
    remaining_text = None
    seen_string = ''
    try_parse_string = ''
    for char in s:
        seen_string += char
        try_parse_string = re.sub(VAR_PATTERN, 'x', seen_string)
        try:
            expr = validator(try_parse_string)
            expr_matches = re.finditer(VAR_PATTERN, seen_string) 
            expr_text = seen_string
            remaining_text = s[len(seen_string):]
        except SyntaxError as e:
            first_error = first_error or e
    if expr is None:
        raise first_error
    matches = list(reversed(list(expr_matches)))
    replace_matches = []
    testidx = 0
    for testidx, match in enumerate(matches):
        teststr = expr_text
        test_matches = [m for m in matches if m is not match]
        for m in test_matches:
            teststr = teststr[:m.start()] + 'x' + teststr[m.end():]
        try:
            validator(teststr)
        except SyntaxError:
            replace_matches.append(match)
    replaced_text = expr_text
    for m in replace_matches:
        old = expr_text[m.start():m.end()]
        replaced_text = replaced_text[:m.start()] + varrepl(old) + replaced_text[m.end():]
    return validator(replaced_text), replaced_text, remaining_text

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

# for val in vals:
#     comp = compile_python_expressions(val)
#     for exp in comp:
#         print(eval(exp[0]))
    