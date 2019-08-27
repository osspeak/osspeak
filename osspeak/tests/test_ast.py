import sys
sys.path.insert(0, '../osspeak')
from recognition.rules import astree, _lark
from recognition import rule, lark_parser
from recognition.lark_parser import utterance_grammar

def test_hello_world():
    text = 'hello world'
    rule_from_string = rule(text)
    lark_ast = utterance_grammar.parse(text)
    rule_from_ast = astree.rule_from_ast(lark_ast)
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
    rule_from_ast = astree.rule_from_ast(lark_ast)
    assert rule_from_ast == rule_from_string