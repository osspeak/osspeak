from lark import Lark

grammar = '''start: ([block] NEWLINE)* [block]
block: (command | rule_definition | comment)
comment: /\s*#.+/
NEWLINE: /\\n/
_SPACE: (" " | "\\t")
_optional_spaces: _SPACE*
NAME: /[a-zA-Z][a-zA-Z0-9]*/
rule_definition: NAME _optional_spaces ":=" _optional_spaces utterance
utterance: (WORD | rule_reference)+
rule_reference: "<" WORD ">"
command: utterance _optional_spaces "=" _optional_spaces action

action: (expr _SPACE+)* expr
expr: (ESCAPED_STRING | binop | expr_grouping | keypress | literal | INTEGER | FLOAT)
expr_grouping: "(" expr ")"
binop: expr _optional_spaces ("+" | "-" | "*" | "/" | "//" | "%" | "==" | "!=") _optional_spaces expr
keypress: "{" "}"
INTEGER: /-?[0-9]+/
FLOAT: /-?([0-9]+)?\.[0-9]+/
literal.-1: /[^{}()\s"'|]+/

%import common.WORD   // imports from terminal library
%import common.ESCAPED_STRING
'''


l = Lark(grammar)

print( l.parse('''f = 4+-3.4''') )