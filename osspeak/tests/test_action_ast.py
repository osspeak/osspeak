import sys
import json
sys.path.insert(0, '../osspeak')
from recognition.actions import astree
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

def test_literal():
    text = "hello \tworld"
    action = text_to_action(text)
    assert_equal(action, {"expressions": [{"type": "String", "value": text}], "type": "Action"})

def test_lists():
    text = "[1, 2] [3]"
    action = text_to_action(text)
    assert_equal(action, {
        "type": "Action",
        "expressions": [
            {"items": [
                {"type": "Integer", "value": 1},
                {"type": "Integer", "value": 2}
            ],
            "type": "List"},
            {"items": [{"type": "Integer", "value": 3}], "type": "List"}
        ],
    })
def test_index():
    text = "[1, 2][3]"
    action = text_to_action(text)
    assert_equal(action,  {
        'expressions': [
            {'index_key': {'type': 'Integer', 'value': 3},
            'index_of': {
                'items': [{'type': 'Integer', 'value': 1}, {'type': 'Integer', 'value': 2}],
                'type': 'List'
            },
        'type': 'Index'}
        ],
        'type': 'Action'
    })

def test_call1():
    text = "repeat({$1}, $2)"
    action = text_to_action(text)
    to_clipboard(action)
    assert_equal(action,  {
        "expressions": [
            {
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
            }
        ],
        "type": "Action"
    })

def test_variable1():
    text = "4 + $1"
    action = text_to_action(text)
    assert_equal(action,  {
        "expressions": [
            {
                "left": {
                    "type": "Integer",
                    "value": 4
                },
                "operation": "add",
                "right": {
                    "type": "Variable",
                    "value": 1
                },
                "type": "BinOp"
            }
        ],
        "type": "Action"
    })

def test_attribute1():
    text = "$1.upper()"
    action = text_to_action(text)
    assert_equal(action, {
        "expressions": [
            {
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
            }
        ],
        "type": "Action"
    })

def test_string1():
    text = "'http://news.ycombinator.com'"
    action = text_to_action(text)
    assert_equal(action,  {
        "expressions": [
            {
                "type": "String",
                "value": "http://news.ycombinator.com"
            }
        ],
        "type": "Action"
    })

def test_binop1():
    text = "4 + 5"
    action = text_to_action(text)
    assert_equal(action,  {
    "expressions": [
        {
            "left": {
                "type": "Integer",
                "value": 4
            },
            "operation": "add",
            "right": {
                "type": "Integer",
                "value": 5
            },
            "type": "BinOp"
        }
    ],
    "type": "Action"
})

def test_float1():
    text = "-4.5 .23 0.2"
    action = text_to_action(text)
    assert_equal(action,  {
    "expressions": [
        {
            "operand": {
                "type": "Float",
                "value": 4.5
            },
            "operation": "usub",
            "type": "UnaryOp"
        },
        {
            "type": "Float",
            "value": 0.23
        },
        {
            "type": "Float",
            "value": 0.2
        }
    ],
    "type": "Action"
})

def test_argument_reference():
    text = "$foo $bar"
    action = text_to_action(text)
    to_clipboard(action)
    assert_equal(action,  {
    "expressions": [
        {
            "type": "ArgumentReference",
            "value": "foo"
        },
        {
            "type": "ArgumentReference",
            "value": "bar"
        }
    ],
    "type": "Action"
})

def to_clipboard(action):
    recognition.actions.library.clipboard.set(astree.to_json_string(action))

def assert_equal(action_node, json_value):
    assert json.loads(astree.to_json_string(action_node)) == json_value


def text_to_action(text):
    lark_ir = lark_parser.parse_action(text)
        # print(lark_ir)
        # print(lark_ir.pretty())
        # print(text)
    return astree.action_from_lark_ir(lark_ir, text)

