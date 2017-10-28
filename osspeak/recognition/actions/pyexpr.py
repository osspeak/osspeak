import collections
import ast
import re

def varrepl(_, num):
    num = int(num)
    if num > 0:
        num -= 1
    return f'context.var({num})'

def keyword_call(kw):
    return f"context._meta.call_or_type('{kw}')"

error_handler_strings = (
    ((r'\$', r'-?\d+'), varrepl),
    (('if', None), keyword_call),
    (('while', None), keyword_call),
)

error_handlers = collections.OrderedDict()
for (before_pattern, after_pattern), handler in error_handler_strings:
    before_pattern = None if before_pattern is None else re.compile(f'(.*)({before_pattern})$')
    after_pattern = None if after_pattern is None else re.compile(f'({after_pattern})(.*)')
    error_handlers[(before_pattern, after_pattern)] = handler

def compile_python_expressions(input_string, validator=lambda expr: True, raise_on_error=True):
    expressions = []
    remaining_text = input_string
    while remaining_text:
        try:
            expr_text, temp_remaining_text = greedy_parse(remaining_text, validator)
        except Exception as e:
            if raise_on_error:
                raise e
            break
        else:
            expressions.append(expr_text)
            remaining_text = temp_remaining_text
    return expressions, remaining_text

def handle_parse_error(before, after):
    for (before_pattern, after_pattern), handler in error_handlers.items():
        start, end = before, after
        handler_args = []
        if before_pattern:
            bmatch = before_pattern.match(before)
            if not bmatch:
                continue
            start = bmatch.group(1)
            handler_args.append(bmatch.group(2))
        if after_pattern:
            amatch = after_pattern.match(after)
            if not amatch:
                continue
            end = amatch.group(2)
            handler_args.append(amatch.group(1))
        return start + handler(*handler_args) + end

def greedy_parse(s, validator):
    assert s
    last_error = None
    expr_text = None
    remaining_text = None
    invalid_expression = False
    try_parse_string = ''
    for i, char in enumerate(s):
        try_parse_string = s[:i + 1] 
        while try_parse_string is not None:
            try:
                expr = ast.parse(try_parse_string, mode='eval')
            except SyntaxError as e:
                if try_parse_string == s:
                    last_error = e
                before, after = try_parse_string[:e.offset], try_parse_string[e.offset:]
                try_parse_string = handle_parse_error(before, after)
            else:
                if not validator(expr):
                    invalid_expression = True
                else:
                    expr_text = try_parse_string
                    remaining_text = s[i + 1:]
                break
        if invalid_expression:
            break
    if not expr_text:
        raise last_error
    return expr_text, remaining_text