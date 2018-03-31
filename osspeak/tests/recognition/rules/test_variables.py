import unittest

from recognition.rules import converter, parser, lexer, tokens
from recognition.rules.astree import GroupingNode, WordNode 
from recognition import rule
from tests.recognition.rules import strings

class TestVariableBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rules = {}
        for rule_name, rule_text in strings.rules:
            cls.rules[rule_name] = rule(rule_text, name=rule_name)

    def test_a(self):
        self.assertEqual(1,1)
        rules = api
