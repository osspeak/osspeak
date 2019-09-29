import sys
import json
sys.path.insert(0, '../osspeak')
from recognition.actions import astree_constructor
import recognition.actions.context
import recognition.actions.library.clipboard
from recognition import lark_parser
from recognition.lark_parser import action_grammar

# def test_escaped_strings():
#     text = r"'he\'ll\"o'"
#     lark_ir = lark_parser.parse_action(text)
#     print(lark_ir.pretty())

# def test_keypress():
#     text = "{ctrl, alt, del}"
#     lark_ir = lark_parser.parse_action(text)
#     print(lark_ir.pretty())

# def test_variables():
#     text = "$3 $-2"
#     lark_ir = lark_parser.parse_action(text)
#     print(lark_ir.pretty())

# def test_call_chain():
#     text = "current_window.something().click()"
#     lark_ir = lark_parser.parse_action(text)
#     print(lark_ir.pretty())

# def test_call_args():
#     text = "mouse.move(7, 8, y=$1, relative = True )"
#     lark_ir = lark_parser.parse_action(text)
#     print(lark_ir.pretty())

# def test_call_args():
#     text = "mouse.move(7, 8, y=$1, relative = True )"
#     lark_ir = lark_parser.parse_action(text)
#     print(lark_ir.pretty())

# def test_call_chain():
#     text = "first.foo.bar.baz()"
#     lark_ir = lark_parser.parse_action(text)

def test_literal1():
    text = "hello there \tworld"
    action = text_to_action(text)
    assert_equal(action, {
        "type": "Literal",
        "value": "hello there \tworld"
    })

def test_literal2():
    text = "Hello ',' $1"
    action = text_to_action(text)
    assert_equal(action, {
        "expressions": [
            {
                "type": "Literal",
                "value": "Hello"
            },
            {
                "type": "ExprSequenceSeparator",
                "value": " "
            },
            {
                "type": "String",
                "value": ","
            },
            {
                "type": "ExprSequenceSeparator",
                "value": " "
            },
            {
                "type": "Variable",
                "value": 1
            }
        ],
        "type": "ExpressionSequence"
    })

def test_call1():
    text = "repeat({$1}, $2)"
    action = text_to_action(text)
    assert_equal(action, {
        "args": [
            {
                "args": [
                    {
                        "type": "Variable",
                        "value": 1
                    }
                ],
                "fn": {
                    "type": "Name",
                    "value": "keypress"
                },
                "kwargs": {},
                "type": "Call"
            },
            {
                "type": "Variable",
                "value": 2
            }
        ],
        "fn": {
            "type": "Name",
            "value": "repeat"
        },
        "kwargs": {},
        "type": "Call"
    })

def test_variable1():
    text = "4 + $1"
    action = text_to_action(text)
    assert_equal(action,  {
        "left": {
            "type": "Integer",
            "value": 4
        },
        "operator": "add",
        "right": {
            "type": "Variable",
            "value": 1
        },
        "type": "BinOp"
    })

def test_attribute1():
    text = "$1.upper()"
    action = text_to_action(text)
    assert_equal(action, {
        "args": [],
        "fn": {
            "attribute_of": {
                "type": "Variable",
                "value": 1
            },
            "name": "upper",
            "type": "Attribute"
        },
        "kwargs": {},
        "type": "Call"
    })

def test_string1():
    text = "'http://news.ycombinator.com'"
    action = text_to_action(text)
    assert_equal(action,  {
        "type": "String",
        "value": "http://news.ycombinator.com"
    })

def test_binop1():
    text = "4 + 5"
    action = text_to_action(text)
    assert_equal(action,  {
        "left": {
            "type": "Integer",
            "value": 4
        },
        "operator": "add",
        "right": {
            "type": "Integer",
            "value": 5
        },
        "type": "BinOp"
    })

def test_float1():
    text = "-4.5 .23 0.2"
    action = text_to_action(text)
    to_clipboard(action)
    assert_equal(action,  {
        "operand": {
            "expressions": [
                {
                    "type": "Float",
                    "value": 4.5
                },
                {
                    "type": "ExprSequenceSeparator",
                    "value": " "
                },
                {
                    "type": "Float",
                    "value": 0.23
                },
                {
                    "type": "ExprSequenceSeparator",
                    "value": " "
                },
                {
                    "type": "Float",
                    "value": 0.2
                }
            ],
            "type": "ExpressionSequence"
        },
        "operation": "usub",
        "type": "UnaryOp"
    })

def test_argument_reference():
    text = "$foo $bar"
    action = text_to_action(text)
    assert_equal(action, {
        "expressions": [
            {
                "type": "ArgumentReference",
                "value": "foo"
            },
            {
                "type": "ExprSequenceSeparator",
                "value": " "
            },
            {
                "type": "ArgumentReference",
                "value": "bar"
            }
        ],
        "type": "ExpressionSequence"
    })

def test_multiple_args():
    text = "loop(hello, 10)"
    action = text_to_action(text)
    assert_equal(action,  {
        "args": [
            {
                "type": "Literal",
                "value": "hello"
            },
            {
                "type": "Integer",
                "value": 10
            }
        ],
        "fn": {
            "type": "Name",
            "value": "loop"
        },
        "kwargs": {},
        "type": "Call"
    })


def test_order_of_operations1():
    text = "1+2*3"
    assert evaluate_action_text(text) == 7

def test_order_of_operations2():
    text = "1+(3*4)-9"
    assert evaluate_action_text(text) == 4

def test_order_of_operations3():
    text = "1+3*4-9"
    assert evaluate_action_text(text) == 4

def evaluate_action_text(text: str):
    action = text_to_action(text)
    to_clipboard(action)
    context = recognition.actions.context.empty_recognition_context()
    return action.evaluate(context)


def to_clipboard(action):
    recognition.actions.library.clipboard.set(astree_constructor.to_json_string(action))

def assert_equal(action_node, json_value):
    assert json.loads(astree_constructor.to_json_string(action_node)) == json_value


def text_to_action(text):
    lark_ir = lark_parser.parse_action(text)
    print(lark_ir.pretty())
    return astree_constructor.action_from_lark_ir(lark_ir, text)

