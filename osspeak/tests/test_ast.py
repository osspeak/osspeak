import sys
sys.path.insert(0, '../osspeak')
print(sys.path)
from recognition.rules import astree
from recognition import rule

def test_foo():
    r = rule('hello world')
    assert 1 == 2