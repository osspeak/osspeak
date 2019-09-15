import sys
import json
sys.path.insert(0, '../osspeak')
from recognition.rules import astree, _lark
from recognition import rule, lark_parser
from recognition.lark_parser import utterance_grammar

def utterance_from_text(text):
    lark_ir = utterance_grammar.parse(text)
    rule_from_lark_ir = astree.rule_from_lark_ir(lark_ir)
    return rule_from_lark_ir

def test_hello_world():
    text = 'hello world'
    rule_from_string = rule(text)
    lark_ast = utterance_grammar.parse(text)
    rule_from_lark_ir = astree.rule_from_lark_ir(lark_ast)
    sequences = rule_from_string.root.sequences
    compare_string_to_ast(text)
    assert len(sequences) == 1
    words = sequences[0]
    assert [type(x) for x in words] == [astree.WordNode, astree.WordNode]
    assert [x.text for x in words] == ['hello', 'world']

def test_top_level_grouping():
    text = 'hello world | goodbye universe'
    compare_string_to_ast(text)

def test_reference():
    text = 'a number <digit>'
    compare_string_to_ast(text)

def test_range():
    text = 'hello_3-5'
    compare_string_to_ast(text)
    
def test_fixed_repetition():
    text = 'hello_3'
    compare_string_to_ast(text)

def test_nested_grouping():
    text = 'hello world | goodbye (universe | solar system)'
    compare_string_to_ast(text)

def test_grouping_sequences():
    r = rule("(at sign='@')")
    sequences = r.root.sequences
    assert len(r.root.sequences) == 1
    assert len(r.root.sequences[0]) == 1
    node_to_test = r.root.sequences[0][0]
    assert len(node_to_test.sequences) == 1

def compare_string_to_ast(text):
    rule_from_string = rule(text)
    lark_ast = utterance_grammar.parse(text)
    rule_from_lark_ir = astree.rule_from_lark_ir(lark_ast)
    assert astree.same_json(rule_from_lark_ir, rule_from_string)

def test_action_substitute():
    text = "go to (google='http://google.com' | reddit='http://reddit.com')"
    utterance = utterance_from_text(text)
    to_clipboard(utterance)
    assert_equal(utterance, {
    "root": {
        "action_substitute": null,
        "repeat_high": 1,
        "repeat_low": 1,
        "sequences": [
            [
                {
                    "action_substitute": null,
                    "repeat_high": 1,
                    "repeat_low": 1,
                    "text": "go",
                    "type": "WordNode"
                },
                {
                    "action_substitute": null,
                    "repeat_high": 1,
                    "repeat_low": 1,
                    "text": "to",
                    "type": "WordNode"
                },
                {
                    "action_substitute": null,
                    "repeat_high": 1,
                    "repeat_low": 1,
                    "sequences": [
                        [
                            {
                                "action_substitute": null,
                                "repeat_high": 1,
                                "repeat_low": 1,
                                "text": "google",
                                "type": "WordNode"
                            }
                        ],
                        [
                            {
                                "action_substitute": null,
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

def utterance_from_text(text):
    lark_ir = lark_parser.parse_utterance(text)
    return astree.rule_from_lark_ir(lark_ir)

def to_clipboard(utterance):
    import recognition.actions.library.clipboard
    recognition.actions.library.clipboard.set(to_json_string(utterance))

def to_json_string(node):
    return json.dumps(node, cls=SimpleJsonEncoder, sort_keys=True, indent=4)

def assert_equal(utterance, json_value):
    assert json.loads(to_json_string(utterance)) == json_value

class SimpleJsonEncoder(json.JSONEncoder):

    def default(self, o):
        d = o.__dict__.copy()
        d['type'] = o.__class__.__name__
        return d