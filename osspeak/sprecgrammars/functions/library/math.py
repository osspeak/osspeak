import operator

# this should be unnecessary
operator_symbols = {
    '+': 'add',
    '-': 'sub',
}

def operation(operator_name, *operands):
    if operator_name in operator_symbols:
        operator_name = operator_symbols[operator_name]
    operator_function = getattr(operator, operator_name)
    return operator_function(*operands)