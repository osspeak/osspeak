import sys
sys.path.insert(0, '../osspeak')
from recognition.rules import astree
from recognition import rule

def test_hello_world():
    r = rule('hello world')
    sequences = r.root.sequences
    assert len(sequences) == 1
    assert [type(x) for x in sequences[0]] == [astree.WordNode, astree.WordNode]

def test_grouping_sequences():
    r = rule("(at sign='@')")
    sequences = r.root.sequences
    assert len(r.root.sequences) == 1
    assert len(r.root.sequences[0]) == 1
    node_to_test = r.root.sequences[0][0]
    assert len(node_to_test.sequences) == 1