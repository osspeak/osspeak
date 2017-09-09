'''
Replace ast.Name nodes with strings wherever possible:
    foo + bar -> 'foo' + 'bar'
    sorted([sjhsdfjsdfsdf, abc, 'de'], key=len) -> sorted(['de', 'abc', 'sjhsdfjsdfsdf'], key=len)

Ignore:
    foo[0], foo[::], foo()
    arguments TODO: fix scope escaping
    locals/globals unless they're direct children of root expression
'''

import ast

class NameToStringTransformer(ast.NodeTransformer):

    def __init__(self, root, namespace, arguments):
        super().__init__()
        self.namespace = namespace
        self.arguments = arguments
        self.nodes_to_replace = self.to_replace(root)
        
    def to_replace(self, root):
        nodes_to_replace = set()
        names_to_keep = set()
        for node in ast.walk(root):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, ast.arg):
                    names_to_keep.add(child.arg)
                if not isinstance(child, ast.Name):
                    continue
                if child.id in self.arguments:
                    names_to_keep.add(child.id)
                    continue
                is_call_or_slice = isinstance(node, (ast.Subscript, ast.Attribute)) or (isinstance(node, ast.Call) and node.func is child)
                if not (is_call_or_slice or 
                    (child.id in self.namespace and node is not root)):
                    nodes_to_replace.add(child)
        return set(n for n in nodes_to_replace if n.id not in names_to_keep)

    def visit_Name(self, node):
        if node in self.nodes_to_replace:
            return ast.Str(s=node.id)
        return node

class SetLiteralTransformer(ast.NodeTransformer):

    def __init__(self):
        super().__init__()
        
    def visit_Set(self, node):
        func = ast.Name(id='keys', ctx=ast.Load())
        return ast.Call(func=func, args=node.elts, keywords=[])

def transform_expression(expr_text, namespace=None, arguments=None):
    arguments = arguments or []
    namespace = get_builtins() if namespace is None else namespace
    expr = ast.parse(expr_text, mode='eval')
    new_expr = NameToStringTransformer(expr, namespace, arguments).visit(expr)
    new_expr = SetLiteralTransformer().visit(new_expr)
    return compile(ast.fix_missing_locations(new_expr), filename=f'<{expr_text}>', mode='eval')

def get_builtins():
    return __builtins__ if isinstance(__builtins__, dict) else dir(__builtins__)