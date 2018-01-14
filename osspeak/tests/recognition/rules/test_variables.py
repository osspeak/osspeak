import unittest

from recognition.rules import converter, parser, lexer, tokens
from recognition.rules.astree import GroupingNode, OrNode, WordNode 
from recognition import api
from tests.recognition.rules import strings

class TestVariableBase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rules = {}
        for rule_name, rule_text in strings.rules:
            rule = api.rule(rule_text, name=rule_name, rules=cls.rules)
            cls.rules[rule_name] = rule

    def test_a(self):
        self.assertEqual(1,1)
        rules = api
