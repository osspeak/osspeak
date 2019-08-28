from lark import Lark, Transformer, v_args, Token, Tree

UTTERANCE_CHOICES = 'utterance_choices'
UTTERANCE_CHOICE_ITEMS = 'utterance_choices_items'
UTTERANCE_WORD = 'utterance_word'
UTTERANCE_REFERENCE = 'utterance_reference'
UTTERANCE_REPETITION = 'utterance_repetition'
UTTERANCE_RANGE = 'utterance_range'

ZERO_OR_POSITIVE_INT = 'ZERO_OR_POSITIVE_INT'

EXPR = '_expr'
VARIABLE = 'variable'

grammar = f'''start: ([block] _NEWLINE)* [block]
block: (command | named_utterance | comment)
comment: /\\s*#.*/
_NEWLINE: /\\n/
NAME: /[_a-zA-Z][_a-zA-Z0-9]*/
named_utterance: utterance_name ":=" utterance
utterance: {UTTERANCE_CHOICE_ITEMS} 
utterance_sequence: utterance_piece ( utterance_piece)*
utterance_piece: ({UTTERANCE_WORD} | {UTTERANCE_REFERENCE} | {UTTERANCE_CHOICES}) [{UTTERANCE_REPETITION}] [action_substitute]
{UTTERANCE_CHOICES}: "(" {UTTERANCE_CHOICE_ITEMS} ")"
{UTTERANCE_CHOICE_ITEMS}: utterance_sequence ( "|" utterance_sequence )* 
utterance_name: /[a-zA-Z_]+/
{UTTERANCE_WORD}: /[a-z0-9]+/
{UTTERANCE_REFERENCE}: "<" utterance_name ">"
action_substitute: "=" action
{UTTERANCE_REPETITION}: "_" ({ZERO_OR_POSITIVE_INT} | {UTTERANCE_RANGE})
{UTTERANCE_RANGE}: {ZERO_OR_POSITIVE_INT} "-" [{ZERO_OR_POSITIVE_INT}]

command: utterance "=" action 

action: {EXPR}+ 
BOOL: ("True" | "False")
{EXPR}: (list | string | binop | expr_grouping | keypress | INTEGER | FLOAT | {VARIABLE} | chain | call | BOOL)
expr_grouping: "(" {EXPR} ")"
binop: {EXPR} ("+" | "-" | "*" | "/" | "//" | "%" | "==" | "!=") {EXPR}
list: "[" [{EXPR} ["," {EXPR}]] "]"
keypress: "{{" {EXPR} ("," {EXPR})* "}}"
{VARIABLE}: "$" INTEGER 
{ZERO_OR_POSITIVE_INT}: /[0-9]+/
INTEGER: /-?[0-9]+/
FLOAT: /-?([0-9]+)?\\.[0-9]+/
literal.-1: /[a-zA-Z]+/
call: NAME "(" ((arg_list ["," kwarg_list]) | [kwarg_list]) ")"
arg_list: {EXPR} ( "," {EXPR})*
kwarg_list: kwarg ( "," kwarg)* 
kwarg: NAME "=" {EXPR}
_chainable: (call | NAME)
chain: _chainable ("." _chainable)+

_STRING_INNER: /.*?/
_STRING_ESC_INNER: _STRING_INNER /(?<!\\\\)(\\\\\\\\)*?/ 
STRING_SINGLE: "'" _STRING_ESC_INNER "'"
STRING_DOUBLE: "\\"" _STRING_ESC_INNER "\\""
string: (STRING_SINGLE | STRING_DOUBLE | literal)

%import common.WORD  // imports from terminal library
%ignore " "
'''

lark_grammar = Lark(grammar)
utterance_grammar = Lark(grammar, start='utterance')
action_grammar = Lark(grammar, start='action')

class Foo(Transformer):

    def string(self, children):
        print(children)
        child = children[0]
        if isinstance(child, Tree) and child.data =='literal':
            return str(child.children[0])
        return child[1:-1]

def parse_utterance(text: str):
    ast = utterance_grammar.parse(text)
    return ast

def parse_action(text: str):
    ast = action_grammar.parse(text)
    transformed = Foo().transform(ast)
    print(ast)
    print(transformed)
    return transformed