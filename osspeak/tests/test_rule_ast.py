import sys
import json
sys.path.insert(0, '../osspeak')
from recognition.rules import astree, _lark
from recognition import rule, lark_parser
from recognition.lark_parser import utterance_grammar

def utterance_from_text(text):
    lark_ir = utterance_grammar.parse(text)
    utterance_from_lark_ir = astree.utterance_from_lark_ir(lark_ir)
    return utterance_from_lark_ir

def test_hello_world():
    text = 'hello world'

def test_top_level_grouping():
    text = 'hello world | goodbye universe'

def test_reference():
    text = 'a number <digit>'

def test_range():
    text = 'hello_3-5'
    
def test_fixed_repetition():
    text = 'hello_3'

def test_nested_grouping():
    text = 'hello world | goodbye (universe | solar system)'

def test_action_substitute2():
    text = "question = how are you | fruit = i like apples"
    utterance = utterance_from_text(text)
    to_clipboard(utterance)
    assert_equal(utterance, {
    "root": {
        "action_substitute": None,
        "ignore_ambiguities": False,
        "repeat_high": 1,
        "repeat_low": 1,
        "sequences": [
            [
                {
                    "action_substitute": {
                        "type": "Literal",
                        "value": "how are you"
                    },
                    "repeat_high": 1,
                    "repeat_low": 1,
                    "text": "question",
                    "type": "WordNode"
                },
            ],
            [
                {
                    "action_substitute": {
                        "type": "Literal",
                        "value": "i like apples"
                    },
                    "repeat_high": 1,
                    "repeat_low": 1,
                    "text": "fruit",
                    "type": "WordNode"
                },
            ]
        ],
        "type": "GroupingNode"
    },
    "type": "Rule"
})

def test_action_substitute():
    text = "go to (google='http://google.com' | reddit='http://reddit.com')"
    utterance = utterance_from_text(text)
    assert_equal(utterance, {
    "root": {
        "action_substitute": None,
        "ignore_ambiguities": False,
        "repeat_high": 1,
        "repeat_low": 1,
        "sequences": [
            [
                {
                    "action_substitute": None,
                    "repeat_high": 1,
                    "repeat_low": 1,
                    "text": "go",
                    "type": "WordNode"
                },
                {
                    "action_substitute": None,
                    "repeat_high": 1,
                    "repeat_low": 1,
                    "text": "to",
                    "type": "WordNode"
                },
                {
                    "action_substitute": None,
                    "ignore_ambiguities": False,
                    "repeat_high": 1,
                    "repeat_low": 1,
                    "sequences": [
                        [
                            {
                                "action_substitute": {
                                    "type": "String",
                                    "value": "http://google.com"
                                },
                                "repeat_high": 1,
                                "repeat_low": 1,
                                "text": "google",
                                "type": "WordNode"
                            }
                        ],
                        [
                            {
                                "action_substitute": {
                                    "type": "String",
                                    "value": "http://reddit.com"
                                },
                                "repeat_high": 1,
                                "repeat_low": 1,
                                "text": "reddit",
                                "type": "WordNode"
                            }
                        ]
                    ],
                    "type": "GroupingNode"
                }
            ]
        ],
        "type": "GroupingNode"
    },
    "type": "Rule"
})

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))

def utterance_from_text(text):
    lark_ir = lark_parser.parse_utterance(text)
    return astree.utterance_from_lark_ir(lark_ir)

def to_clipboard(utterance):
    import recognition.actions.library.clipboard
    s = to_json_string(utterance)
    formatted = to_json_string(json.loads(s))
    recognition.actions.library.clipboard.set(formatted.replace('null', 'None').replace('false', 'False').replace('true', 'True'))

def to_json_string(node):
    return json.dumps(node, cls=SimpleJsonEncoder, sort_keys=True, indent=4)

def assert_equal(utterance, json_value):
    assert json.loads(to_json_string(utterance)) == json_value

class SimpleJsonEncoder(json.JSONEncoder):

    def default(self, o):
        d = o.__dict__.copy()
        d['type'] = o.__class__.__name__
        return d