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

    def __init__(self, root):
        super().__init__()
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
                if not (isinstance(node, (ast.Subscript, ast.Attribute)) or
                    (isinstance(node, ast.Call) and node.func is child) or 
                    (child.id in __builtins__ and node is not root)):
                    nodes_to_replace.add(child)
        return set(n for n in nodes_to_replace if n.id not in names_to_keep)

    def visit_Name(self, node):
        if node in self.nodes_to_replace:
            return ast.Str(s=node.id)
        return node

def transform_expression(expr_text):
    expr = ast.parse(expr_text, mode='eval')
    new_expr = NameToStringTransformer(expr).visit(expr)
    return compile(ast.fix_missing_locations(new_expr), filename='<ast>', mode='eval')