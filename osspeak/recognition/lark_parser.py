from lark import Lark

grammar = '''start: ([block] _NEWLINE)* [block]
block: (command | named_utterance | comment)
comment: /\s*#.*/
_NEWLINE: /\\n/
_SPACE: (" " | "\\t")
_optsp: _SPACE*
NAME: /[a-zA-Z][a-zA-Z0-9]*/
named_utterance: NAME _optsp ":=" _optsp utterance
utterance: utterance_piece (_SPACE utterance_piece)*
utterance_piece: (WORD | utterance_reference | utterance_choices) [repetition] [action_substitute]
utterance_choices: "(" _optsp utterance_choices_items _optsp ")"
utterance_choices_items: utterance (_optsp "|" _optsp utterance _optsp)* 
utterance_reference: "<" WORD ">"
action_substitute: "=" _optsp action
repetition: "_" (ZERO_OR_POSITIVE_INT | range)
range: ZERO_OR_POSITIVE_INT ".." ZERO_OR_POSITIVE_INT

command: _optsp utterance _optsp "=" _optsp action _optsp

action: (expr _SPACE+)* expr
expr: (ESCAPED_STRING | binop | expr_grouping | keypress | literal | INTEGER | FLOAT)
expr_grouping: "(" expr ")"
binop: expr _optsp ("+" | "-" | "*" | "/" | "//" | "%" | "==" | "!=") _optsp expr
keypress: "{" expr ("," _optsp expr)* "}"
ZERO_OR_POSITIVE_INT: /[0-9]+/
INTEGER: /-?[0-9]+/
FLOAT: /-?([0-9]+)?\.[0-9]+/
literal.-1: /[^,{}()\s"'|]+/

%import common.WORD   // imports from terminal library
%import common.ESCAPED_STRING
'''


lark_grammar = Lark(grammar)