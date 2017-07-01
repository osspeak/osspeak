import operator

# this should be unnecessary
operator_symbols = {
    '+': 'add',
    '-': 'sub',
    '*': 'mul',
    '/': 'truediv',
    '//': 'floordiv',
    '%': 'mod',
    '**': 'pow',
    '>=': 'ge',
    '>': 'gt',
    '<': 'lt',
    '<=': 'le',
    '!=': 'ne',
    '==': 'eq',
}

def operation(operator_name, *operands):
    print('abc', operator, operands)
    if operator_name in operator_symbols:
        operator_name = operator_symbols[operator_name]
    operator_function = getattr(operator, operator_name)
    return operator_function(*operands)