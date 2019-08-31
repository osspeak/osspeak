import lark.lexer
import lark.tree
import json

class BaseActionNode:
    
    def perform(self):
        raise NotImplementedError

class Action(BaseActionNode):

    def __init__(self, expressions):
        self.expressions = expressions

class String(BaseActionNode):

    def __init__(self, value: str):
        self.value = value

def action_from_lark_ir(root_lark_ir):
    expressions = []
    for child in root_lark_ir.children:
        expr = parse_expr(child)
        expressions.append(expr)
    return Action(expressions)

def to_json(action):
    return json.dumps(action, cls=ActionEncoder, sort_keys=True)

def parse_expr(lark_ir):
    print(type(lark_ir))
    if isinstance(lark_ir, lark.tree.Tree):
        if lark_ir.data == 'literal':
            return String(lark_ir.children[0])
            print('tree')
    print(lark_ir)
    raise ValueError(f'Unrecognized expression: {lark_ir.pretty()}')

class ActionEncoder(json.JSONEncoder):

    def default(self, o):
        d = o.__dict__.copy()
        d['type'] = o.__class__.__name__
        # try:
        #     del d['action_piece_substitute']
        # except KeyError:
        #     pass
        return d