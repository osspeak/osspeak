import ast
import re

def varrepl(matched_text):
    num = int(matched_text[1:])
    if num > 0:
        num -= 1
    return f'result.vars.get({num})'

VAR_PATTERN = re.compile(r'\$-?\d+')
VAR_PATTERN_END = re.compile(r'\$-?\d+$')

def compile_python_expressions(input_string, validator=lambda expr: True, raise_on_error=True):
    expressions = []
    remaining_text = input_string
    while remaining_text:
        try:
            expr_text, remaining_text = greedy_parse(remaining_text, validator)
        except Exception as e:
            if raise_on_error:
                raise e
            else:
                break
        expressions.append(expr_text)
    return expressions

def greedy_parse(s, validator):
    assert s
    first_error = None
    expr_text = None
    expr_matches = None
    remaining_text = None
    seen_string = ''
    for char in s:
        seen_string += char
        try_parse_string = re.sub(VAR_PATTERN, 'variables[0]', seen_string)
        try:
            expr = ast.parse(try_parse_string, mode='eval')
        except SyntaxError as e:
            first_error = first_error or e
        else:
            if not validator(expr):
                remaining_text = None
                break
            expr_matches = re.finditer(VAR_PATTERN, seen_string) 
            expr_text = seen_string
            remaining_text = s[len(seen_string):]
    if expr_text is None:
        raise first_error
    replaced_text = replace_matches(expr_matches, expr_text)
    return replaced_text, remaining_text

def replace_matches(matches, expr_text):
    '''
    find which $int matches we need to replace (Names) and which we
    don't (inside strings). Then replace whichever matches raised
    syntax errors
    '''
    replace_matches = []
    # replace in reversed order to preserve positions of earlier matches
    matches = list(reversed(list(matches)))
    for match in matches:
        teststr = expr_text
        test_matches = (m for m in matches if m is not match)
        for m in test_matches:
            teststr = teststr[:m.start()] + 'variables[0]' + teststr[m.end():]
        try:
            ast.parse(teststr, mode='eval')
        except SyntaxError:
            replace_matches.append(match)
    # replace the matches that raised syntax error if not changed
    replaced_text = expr_text
    for m in replace_matches:
        old = expr_text[m.start():m.end()]
        assert VAR_PATTERN_END.match(old)
        replaced_text = replaced_text[:m.start()] + varrepl(old) + replaced_text[m.end():]
    return replaced_text
    