import ast
import re

def varrepl(_, num):
    num = int(num)
    if num > 0:
        num -= 1
    return f'result.vars.get({num})'

error_handler_strings = {
    (r'\$', r'-?\d+'): varrepl
}

error_handlers = {}
for (before_pattern, after_pattern), handler in error_handler_strings.items():
    before_pattern = None if before_pattern is None else re.compile(f'(.*)({before_pattern})$')
    after_pattern = None if after_pattern is None else re.compile(f'({after_pattern})(.*)')
    error_handlers[(before_pattern, after_pattern)] = handler

def compile_python_expressions(input_string, validator=lambda expr: True, raise_on_error=True):
    expressions = []
    remaining_text = input_string
    while remaining_text:
        try:
            expr_text, remaining_text = greedy_parse(remaining_text, validator)
        except Exception as e:
            remaining_text = handle_parse_error(remaining_text[:e.offset], remaining_text[e.offset:])
            if remaining_text is None:
                if raise_on_error:
                    raise e
                break
        else:
            expressions.append(expr_text)
    expressions = merge_expressions(expressions)
    return expressions

def merge_expressions(expressions):
    merged = []
    for expr in expressions:
        if not merged:
            merged.append(expr)
        else:
            merged_expr = merged[-1] + expr
            try:
                ast.parse(merged_expr, mode='eval')
            except:
                merged.append(expr)
            else:
                merged[-1] = merged_expr
    return merged

def handle_parse_error(before, after):
    for (before_pattern, after_pattern), handler in error_handlers.items():
        start, end = before, after
        before_error_text, after_error_text = None, None
        if before_pattern:
            bmatch = before_pattern.match(before)
            if not bmatch:
                break
            start, before_error_text = bmatch.group(1), bmatch.group(2)
        if after_pattern:
            amatch = after_pattern.match(after)
            if not amatch:
                break
            after_error_text, after = amatch.group(1), amatch.group(2)
        return start + handler(before_error_text, after_error_text) + after

def greedy_parse(s, validator):
    assert s
    last_error = None
    expr_text = None
    remaining_text = None
    seen_string = ''
    for char in s:
        seen_string += char
        try:
            expr = ast.parse(seen_string, mode='eval')
        except SyntaxError as e:
            last_error = e
        else:
            if not validator(expr):
                remaining_text = None
                break
            expr_text = seen_string
            remaining_text = s[len(seen_string):]
    if expr_text is None:
        raise last_error
    return expr_text, remaining_text