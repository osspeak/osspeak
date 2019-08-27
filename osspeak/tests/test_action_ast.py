import sys
sys.path.insert(0, '../osspeak')
from recognition.rules import astree, _lark
from recognition import lark_parser
from recognition.lark_parser import action_grammar

def test_escaped_strings():
    text = r"'he\'ll\"o'"
    ast = lark_parser.parse_action(text)
    print(ast.pretty())

def test_keypress():
    text = "{ctrl, alt, del}"
    ast = lark_parser.parse_action(text)
    print(ast.pretty())

def test_variables():
    text = "$3 $-2"
    ast = lark_parser.parse_action(text)
    print(ast.pretty())
def test_call_chain():
    text = "current_window.something().click()"
    ast = lark_parser.parse_action(text)
    print(ast.pretty())

def test_call_args():
    text = "mouse.move(7, 8, y=$1, relative = True )"
    ast = lark_parser.parse_action(text)
    print(ast.pretty())

