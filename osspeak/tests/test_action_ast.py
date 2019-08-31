import sys
import json
sys.path.insert(0, '../osspeak')
from recognition.actions import astree
from recognition import lark_parser
from recognition.lark_parser import action_grammar

def test_escaped_strings():
    text = r"'he\'ll\"o'"
    lark_ir = lark_parser.parse_action(text)
    print(lark_ir.pretty())

def test_keypress():
    text = "{ctrl, alt, del}"
    lark_ir = lark_parser.parse_action(text)
    print(lark_ir.pretty())

def test_variables():
    text = "$3 $-2"
    lark_ir = lark_parser.parse_action(text)
    print(lark_ir.pretty())

def test_call_chain():
    text = "current_window.something().click()"
    lark_ir = lark_parser.parse_action(text)
    print(lark_ir.pretty())

def test_call_args():
    text = "mouse.move(7, 8, y=$1, relative = True )"
    lark_ir = lark_parser.parse_action(text)
    print(lark_ir.pretty())

def test_call_args():
    text = "mouse.move(7, 8, y=$1, relative = True )"
    lark_ir = lark_parser.parse_action(text)
    print(lark_ir.pretty())

def test_call_chain():
    text = "first.foo.bar.baz()"
    lark_ir = lark_parser.parse_action(text)

def test_basic():
    text = "hello world"
    action = text_to_action(text)
    assert_equal(action, {"expressions": [{"type": "String", "value": "hello"}, {"type": "String", "value": "world"}], "type": "Action"})

def test_foo():
    text = "!@"
    action = text_to_action(text)
    assert_equal(action, {})


def assert_equal(action_node, json_value):
    assert json.loads(astree.to_json(action_node)) == json_value


def text_to_action(text):
    lark_ir = lark_parser.parse_action(text)
    print(lark_ir)
    print(lark_ir.pretty())
    return astree.action_from_lark_ir(lark_ir)

