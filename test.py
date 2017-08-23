import ast

s = f'a{$1}b'

r = compile('f"hello {$1}"', filename='<ast>', mode='eval')