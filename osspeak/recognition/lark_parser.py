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
_SPACE: (" " | "\\t")
_optsp: _SPACE*
NAME: /[_a-zA-Z][_a-zA-Z0-9]*/
named_utterance: utterance_name _optsp ":=" _optsp utterance
utterance: _optsp {UTTERANCE_CHOICE_ITEMS} _optsp
utterance_sequence: utterance_piece (_optsp utterance_piece)*
utterance_piece: ({UTTERANCE_WORD} | {UTTERANCE_REFERENCE} | {UTTERANCE_CHOICES}) [{UTTERANCE_REPETITION}] [action_substitute]
{UTTERANCE_CHOICES}: "(" _optsp {UTTERANCE_CHOICE_ITEMS} _optsp ")"
{UTTERANCE_CHOICE_ITEMS}: utterance_sequence (_optsp "|" _optsp utterance_sequence _optsp)* 
utterance_name: /[a-z]+/
{UTTERANCE_WORD}: /[a-z]+/
{UTTERANCE_REFERENCE}: "<" utterance_name ">"
action_substitute: "=" _optsp action
{UTTERANCE_REPETITION}: "_" ({ZERO_OR_POSITIVE_INT} | {UTTERANCE_RANGE})
{UTTERANCE_RANGE}: {ZERO_OR_POSITIVE_INT} "-" {ZERO_OR_POSITIVE_INT}

command: utterance "=" _optsp action _optsp

action: _optsp ({EXPR} _SPACE+)* {EXPR} _optsp
BOOL: ("True" | "False")
{EXPR}: (string | binop | expr_grouping | keypress | INTEGER | FLOAT | {VARIABLE} | chain | call | BOOL)
expr_grouping: "(" {EXPR} ")"
binop: {EXPR} _optsp ("+" | "-" | "*" | "/" | "//" | "%" | "==" | "!=") _optsp {EXPR}
keypress: "{{" {EXPR} ("," _optsp {EXPR})* "}}"
{VARIABLE}: "$" INTEGER 
{ZERO_OR_POSITIVE_INT}: /[0-9]+/
INTEGER: /-?[0-9]+/
FLOAT: /-?([0-9]+)?\\.[0-9]+/
literal.-1: /[a-zA-Z]+/
call: NAME "(" _optsp ((arg_list ["," _optsp kwarg_list]) | [kwarg_list]) _optsp ")"
arg_list: {EXPR} ( _optsp "," _optsp {EXPR})*
kwarg_list: kwarg ( _optsp "," _optsp kwarg)* 
kwarg: NAME _optsp "=" _optsp {EXPR}
_chainable: (call | NAME)
chain: _chainable ("." _chainable)+

_STRING_INNER: /.*?/
_STRING_ESC_INNER: _STRING_INNER /(?<!\\\\)(\\\\\\\\)*?/ 
STRING_SINGLE: "'" _STRING_ESC_INNER "'"
STRING_DOUBLE: "\\"" _STRING_ESC_INNER "\\""
string: (STRING_SINGLE | STRING_DOUBLE | literal)

%import common.WORD   // imports from terminal library
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

def parse_action(text: str):
    ast = action_grammar.parse(text)
    transformed = Foo().transform(ast)
    print(ast)
    print(transformed)
    return transformed