import unittest

from sprecgrammars.formats.rules import converter, parser 
from sprecgrammars.formats.rules.astree import GroupingNode, OrNode, WordNode 
from tests.sprecgrammars.rules import strings

class TestRuleParser(unittest.TestCase):

    def parse_rule(self, rule_string):
        rule_parser = parser.RuleParser(rule_string)
        rule = rule_parser.parse_as_rule()
        return rule

    def test_grouping1(self):
        rule = self.parse_rule(strings.GROUPING1)
        self.assertEqual(len(rule.children), 1)
        self.assertIsInstance(rule.children[0], GroupingNode)
        self.assertEqual(len(rule.children[0].children), 2)
        self.assertEqual(rule.children[0].children[0].text, 'hello')
        self.assertEqual(len(rule.children[0].children[1].children), 3)
        self.assertEqual(rule.children[0].children[1].children[0].text, 'world')
        self.assertIsInstance(rule.children[0].children[1].children[1], OrNode)
        self.assertEqual(rule.children[0].children[1].children[2].text, 'universe')
