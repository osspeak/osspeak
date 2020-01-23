from lark import Lark, Transformer, v_args, Token, Tree

UTTERANCE_CHOICES = 'utterance_choices'
UTTERANCE_CHOICES_OPTIONAL = 'utterance_choices_optional'
UTTERANCE_CHOICE_ITEMS = 'utterance_choices_items'
UTTERANCE_WORD = 'UTTERANCE_WORD'
IGNORE_AMBIGUITIES = 'IGNORE_AMBIGUITIES'
UTTERANCE_REFERENCE = 'utterance_reference'
UTTERANCE_REPETITION = 'utterance_repetition'
UTTERANCE_RANGE = 'utterance_range'
UTTERANCE_NAME = 'utterance_name'
ACTION_SUBSTITUTE = 'action_substitute'

ZERO_OR_POSITIVE_INT = 'ZERO_OR_POSITIVE_INT'

EXPR = 'expr'
EXPR_SEQUENCE = 'expr_sequence'
EXPR_SEQUENCE_SEPARATOR = 'EXPR_SEQUENCE_SEPARATOR'
SLICE_SEPARATOR = 'SLICE_SEPARATOR'
VARIABLE = 'variable'
ARG_LIST = 'arg_list'
KWARG_LIST = 'kwarg_list'
UNARY_OPERATOR = 'UNARY_OPERATOR'
ARGUMENT_REFERENCE = 'argument_reference'
SLICE = 'slice'

grammar = f'''start: ([_block] _NEWLINE)* [_block]
_block: (command | function_definition | named_utterance | comment)
comment: /[ \t]*#.*/
_WS: /[ \t]/
WS: /[ \t]/
NO_WS_AHEAD: /(?![ \t])/
NO_WS_BEHIND: /(?<![ \t])/

_NEWLINE: /\\n/
NAME: /[_a-zA-Z][_a-zA-Z0-9]*/
named_utterance: {UTTERANCE_NAME} ":=" utterance
utterance: {UTTERANCE_CHOICE_ITEMS} 
utterance_sequence: utterance_piece (_WS+ utterance_piece)*
utterance_piece.-101: ({UTTERANCE_WORD} | {UTTERANCE_REFERENCE} | {UTTERANCE_CHOICES} | {UTTERANCE_CHOICES_OPTIONAL}) [{UTTERANCE_REPETITION}] [{ACTION_SUBSTITUTE}]
{UTTERANCE_CHOICES_OPTIONAL}: [{IGNORE_AMBIGUITIES}] "[" {UTTERANCE_CHOICE_ITEMS} "]"
{UTTERANCE_CHOICES}: [{IGNORE_AMBIGUITIES}] "(" {UTTERANCE_CHOICE_ITEMS} ")"
{UTTERANCE_CHOICE_ITEMS}: utterance_sequence ("|" utterance_sequence)* 
{UTTERANCE_NAME}: NAME
{UTTERANCE_WORD}: /[a-z0-9]+/
{UTTERANCE_REFERENCE}: [{IGNORE_AMBIGUITIES}] "<" {UTTERANCE_NAME} ">"
{ACTION_SUBSTITUTE}: "=" _action
!{UTTERANCE_REPETITION}: (("_" ({ZERO_OR_POSITIVE_INT} | {UTTERANCE_RANGE})) | "*" | "?" | "+")
{UTTERANCE_RANGE}: {ZERO_OR_POSITIVE_INT} "-" [{ZERO_OR_POSITIVE_INT}]
{IGNORE_AMBIGUITIES}: "_" NO_WS_AHEAD

command: utterance "=" _action 

_action: ({EXPR} | {EXPR_SEQUENCE})
_grouping.29: "(" {EXPR} ")"
loop: {EXPR} _LOOP_SEPARATOR {EXPR}
{EXPR_SEQUENCE_SEPARATOR}: /[ \t]+/
{EXPR_SEQUENCE}.-99: {EXPR} ({EXPR_SEQUENCE_SEPARATOR} {EXPR})+
{EXPR}: [{UNARY_OPERATOR}] (left_to_right | right_to_left | _other_expr)
_chainable: (NAME | attribute | call | list | {VARIABLE} | {ARGUMENT_REFERENCE} | index | {SLICE})
LEFT_TO_RIGHT_OPERATOR: ("+" | "-" | "*" | "/" | "//" | "%" | "==")
RIGHT_TO_LEFT_OPERATOR: "**"
left_to_right: {EXPR} LEFT_TO_RIGHT_OPERATOR (right_to_left | _other_expr)
right_to_left: {EXPR} RIGHT_TO_LEFT_OPERATOR {EXPR}
_other_expr: ({EXPR_SEQUENCE} | index | {SLICE} | loop | _grouping | attribute | literal | list | STRING_SINGLE | STRING_DOUBLE | keypress | INTEGER | FLOAT | {VARIABLE} | call | {ARGUMENT_REFERENCE})
{UNARY_OPERATOR}: ("+" | "-")
keypress: "{{" {EXPR} ("," {EXPR})* "}}"
_VAR_PREC: "$" NO_WS_AHEAD
_LOOP_SEPARATOR: NO_WS_BEHIND "~" NO_WS_AHEAD
_ATTR_SEPARATOR: NO_WS_BEHIND "." NO_WS_AHEAD
_SUBSCRIPT_PREFIX: NO_WS_BEHIND "["
SLICE_SEPARATOR: ":"
_CALL_START: NO_WS_BEHIND "("
{VARIABLE}: _VAR_PREC INTEGER
{ARGUMENT_REFERENCE}: _VAR_PREC NAME
{ZERO_OR_POSITIVE_INT}: /[0-9]+/
INTEGER: /-?[0-9]+/
LITERAL_PIECE: /[a-zA-Z0-9!]+/ 
literal.-100: LITERAL_PIECE (WS+ LITERAL_PIECE)*

list: "[" [{EXPR} ("," {EXPR})*] "]"
index: _chainable _SUBSCRIPT_PREFIX {EXPR} "]"
{SLICE}: _chainable _SUBSCRIPT_PREFIX [{EXPR}] SLICE_SEPARATOR [{EXPR}] [SLICE_SEPARATOR [{EXPR}]] "]"
attribute.20: _chainable  _ATTR_SEPARATOR NAME
call.30: _chainable _CALL_START (({ARG_LIST} ["," {KWARG_LIST}]) | [{KWARG_LIST}]) ")"
{ARG_LIST}: {EXPR} ("," {EXPR})*
{KWARG_LIST}: kwarg ("," kwarg)* 
kwarg: NAME "=" {EXPR}

function_definition: NAME "(" [positional_parameters] ")" "=>" _action
positional_parameters: NAME ("," NAME)*

_STRING_INNER: /.*?/
_STRING_ESC_INNER: _STRING_INNER /(?<!\\\\)(\\\\\\\\)*?/ 
STRING_SINGLE: "'" _STRING_ESC_INNER "'"
STRING_DOUBLE: "\\"" _STRING_ESC_INNER "\\""

%import common.WORD  // imports from terminal library
%import common.FLOAT  // imports from terminal library
%ignore " "
'''

lark_grammar = Lark(grammar, propagate_positions=True)
utterance_grammar = Lark(grammar, start='utterance', propagate_positions=True)
action_grammar = Lark(grammar, start='_action', propagate_positions=True)

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
    return ast.children[0]
    transformed = Foo().transform(ast)
    return transformed

def lark_node_type(lark_ir):
    type_attr = 'data' if isinstance(lark_ir, Tree) else 'type'
    return getattr(lark_ir, type_attr)

def lark_node_text(lark_ir, text_by_line):
    text = 'foo'
    start_line, end_line = text_by_line[lark_ir.line - 1], text_by_line[lark_ir.end_line - 1]
    if lark_ir.line == lark_ir.end_line:
        text = start_line[lark_ir.column - 1:lark_ir.end_column - 1]
    return text

def find_type(lark_tree, _type):
    for child in getattr(lark_tree, 'children', []):
        if child is not None:
            child_type_attr = 'data' if isinstance(child, Tree) else 'type'
            child_type = getattr(child, child_type_attr)
            if child_type == _type:
                return child
