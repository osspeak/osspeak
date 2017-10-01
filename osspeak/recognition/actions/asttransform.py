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
from recognition import library

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
        return self.generic_visit(node)

class SetLiteralTransformer(ast.NodeTransformer):

    def visit_Set(self, node):
        func = ast.Name(id='keys', ctx=ast.Load())
        return ast.Call(func=func, args=node.elts, keywords=[])

class LambdaArgTransformer(ast.NodeTransformer):

    def visit_Call(self, node):
        func = ast.Name(id='keys', ctx=ast.Load())
        path = node_path(node.func)
        if path in library.lambda_arguments:
            newargs = []
            for arg in node.args:
                largs = ast.arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[])
                newarg = ast.Lambda(args=largs, body=arg)
                newargs.append(newarg)
            node.args = newargs
        return self.generic_visit(node)

class VariableArgumentTransformer(ast.NodeTransformer):

    def __init__(self, root):
        self.parent_map = self.build_parent_map(root)
        
    def visit_Call(self, node):
        if self.is_variable_call(node):
            path = self.get_containing_function_path(node)
            if path:
                func = path[0]
                # only type results for certain arguments. ex: 'foo' in repeat('foo', 10), but not 10 
                if node_path(func) != ('repeat',) or func.args[-1] is path[1]:
                    node.keywords.append(ast.keyword(arg='perform_results', value=ast.NameConstant(value=False)))
        return self.generic_visit(node)

    def build_parent_map(self, root):
        parent_map = {root: None}
        for node in ast.walk(root):
            for child in ast.iter_child_nodes(node):
                parent_map[child] = node
        return parent_map

    def is_variable_call(self, node):
        return isinstance(node, ast.Call) and node_path(node.func) == ('context', 'var')

    def get_containing_function_path(self, node):
        path = [node]
        while node:
            parent = self.parent_map[node]
            path.append(parent)
            if isinstance(parent, ast.Call) and not self.is_variable_call(parent):
                return path[::-1]
            node = parent


def node_path(node):
    if isinstance(node, ast.Call):
        return node_path(node.func)
    if isinstance(node, ast.Name):
        return node.id,
    return node_path(node.value) + (node.attr,)

def transform_expression(expr_text, namespace=None, arguments=None):
    arguments = arguments or []
    namespace = get_builtins() if namespace is None else namespace
    expr = ast.parse(expr_text, mode='eval')
    new_expr = NameToStringTransformer(expr, namespace, arguments).visit(expr)
    new_expr = SetLiteralTransformer().visit(new_expr)
    new_expr = LambdaArgTransformer().visit(new_expr)
    new_expr = VariableArgumentTransformer(new_expr).visit(new_expr)
    return compile(ast.fix_missing_locations(new_expr), filename=f'<{expr_text}>', mode='eval')

def get_builtins():
    return __builtins__ if isinstance(__builtins__, dict) else dir(__builtins__)