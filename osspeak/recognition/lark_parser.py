from lark import Lark, Transformer, v_args, Token, Tree

UTTERANCE_CHOICES = 'utterance_choices'
UTTERANCE_CHOICE_ITEMS = 'utterance_choices_items'
UTTERANCE_WORD = 'UTTERANCE_WORD'
UTTERANCE_REFERENCE = 'utterance_reference'
UTTERANCE_REPETITION = 'utterance_repetition'
UTTERANCE_RANGE = 'utterance_range'
UTTERANCE_NAME = 'utterance_name'

ZERO_OR_POSITIVE_INT = 'ZERO_OR_POSITIVE_INT'

EXPR = 'expr'
VARIABLE = 'variable'
ARG_LIST = 'arg_list'
KWARG_LIST = 'kwarg_list'
UNARY_OPERATOR = 'UNARY_OPERATOR'

grammar = f'''start: ([_block] _NEWLINE)* [_block]
_block: (command | function_definition |     named_utterance | comment)
comment: /[ \t]*#.*/
_WS: /[ \t]+/
WS: /[ \t]+/
_NEWLINE: /\\n/
NAME: /[_a-zA-Z][_a-zA-Z0-9]*/
named_utterance: {UTTERANCE_NAME} ":=" utterance
utterance: {UTTERANCE_CHOICE_ITEMS} 
utterance_sequence: utterance_piece (_WS utterance_piece)*
utterance_piece: ({UTTERANCE_WORD} | {UTTERANCE_REFERENCE} | {UTTERANCE_CHOICES}) [{UTTERANCE_REPETITION}] [action_substitute]
{UTTERANCE_CHOICES}: "(" {UTTERANCE_CHOICE_ITEMS} ")"
{UTTERANCE_CHOICE_ITEMS}: utterance_sequence ("|" utterance_sequence)* 
{UTTERANCE_NAME}: NAME
{UTTERANCE_WORD}: /[a-z0-9]+/
{UTTERANCE_REFERENCE}: "<" {UTTERANCE_NAME} ">"
action_substitute: "=" action
{UTTERANCE_REPETITION}: "_" ({ZERO_OR_POSITIVE_INT} | {UTTERANCE_RANGE})
{UTTERANCE_RANGE}: {ZERO_OR_POSITIVE_INT} "-" [{ZERO_OR_POSITIVE_INT}]

command: utterance "=" action 

action: {EXPR} (_WS {EXPR})*
BOOL: ("True" | "False")
{EXPR}: [{UNARY_OPERATOR}] (index | attribute | literal | list | STRING_SINGLE | STRING_DOUBLE | binop | expr_grouping | keypress | INTEGER | FLOAT | {VARIABLE} | call | BOOL)
_chainable: (NAME | attribute | call | index | list | {VARIABLE})
expr_grouping: "(" {EXPR} ")"
BINARY_OPERATOR: ("+" | "-" | "*" | "/" | "//" | "%" | "==" | "!=")
{UNARY_OPERATOR}: ("+" | "-")
binop.2: {EXPR} BINARY_OPERATOR {EXPR}
keypress: "{{" {EXPR} ("," {EXPR})* "}}"
{VARIABLE}: "$" INTEGER 
{ZERO_OR_POSITIVE_INT}: /[0-9]+/
INTEGER: /-?[0-9]+/
FLOAT: SIGNED_FLOAT
LITERAL_PIECE: /[a-zA-Z0-9]+/ 
literal.-100: LITERAL_PIECE (WS LITERAL_PIECE)*

list: "[" [{EXPR} ["," {EXPR}]] "]"
index.-3: _chainable "[" {EXPR} "]"
attribute.2: _chainable "." NAME
call.3: _chainable "(" (({ARG_LIST} ["," {KWARG_LIST}]) | [{KWARG_LIST}]) ")"
{ARG_LIST}: {EXPR} ("," {EXPR})*
{KWARG_LIST}: kwarg ("," kwarg)* 
kwarg: NAME "=" {EXPR}

function_definition: NAME "(" [positional_parameters] ")" "=>" action
positional_parameters: NAME ("," NAME)*

_STRING_INNER: /.*?/
_STRING_ESC_INNER: _STRING_INNER /(?<!\\\\)(\\\\\\\\)*?/ 
STRING_SINGLE: "'" _STRING_ESC_INNER "'"
STRING_DOUBLE: "\\"" _STRING_ESC_INNER "\\""

%import common.WORD  // imports from terminal library
%import common.SIGNED_FLOAT  // imports from terminal library
%ignore " "
'''

lark_grammar = Lark(grammar, propagate_positions=True)
utterance_grammar = Lark(grammar, start='utterance', propagate_positions=True)
action_grammar = Lark(grammar, start='action', propagate_positions=True)

class Foo(Transformer):

    def string(self, children):
        child = children[0]
        if isinstance(child, Tree) and child.data =='literal':
            return str(child.children[0])
        return child[1:-1]

def parse_command_module(text: str):
    ir = lark_grammar.parse(text)
    return ir
    
def parse_utterance(text: str):
    ast = utterance_grammar.parse(text)
    return ast

def parse_action(text: str):
    ast = action_grammar.parse(text)
    return ast
    transformed = Foo().transform(ast)
    return transformed

def lark_node_type(lark_ir):
    type_attr = 'data' if isinstance(lark_ir, Tree) else 'type'
    return getattr(lark_ir, type_attr)

def lark_node_text(lark_ir, text):
    return 'foo'

def find_type(lark_tree, _type):
    for child in lark_tree.children:
        child_type_attr = 'data' if isinstance(child, Tree) else 'type'
        child_type = getattr(child, child_type_attr)
        if child_type == _type:
            return child
