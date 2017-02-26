import unittest

from sprecgrammars.rules import converter, parser 
from sprecgrammars.rules.astree import GroupingNode, OrNode, WordNode 
from sprecgrammars.actions import nodes
from tests.sprecgrammars.rules import strings

class TestRuleParserBase(unittest.TestCase):

    @property
    def rule(self):
        rule_parser = parser.RuleParser(self.text)
        ruleobj = rule_parser.parse_as_rule()
        return ruleobj

class TestRuleGrouping1(TestRuleParserBase):

    @classmethod
    def setUpClass(cls):
        cls.text = strings.GROUPING1

    def test_grouping1(self):
        rule = self.rule
        self.assertEqual(len(rule.children), 1)
        self.assertIsInstance(rule.children[0], GroupingNode)
        self.assertEqual(len(rule.children[0].children), 2)
        self.assertEqual(rule.children[0].children[0].text, 'hello')
        self.assertEqual(len(rule.children[0].children[1].children), 3)
        self.assertEqual(rule.children[0].children[1].children[0].text, 'world')
        self.assertIsInstance(rule.children[0].children[1].children[1], OrNode)
        self.assertEqual(rule.children[0].children[1].children[2].text, 'universe')

class TestRuleSubstitute1(TestRuleParserBase):

    @classmethod
    def setUpClass(cls):
        cls.text = strings.SUBSTITUTE1

    @property
    def grouping(self):
        return self.rule.children[0]

    def test_first_action(self):
        first_action = self.grouping.children[0].action_substitute
        self.assertIsInstance(first_action, nodes.RootAction)
        self.assertIsInstance(first_action.children[0], nodes.LiteralKeysAction)
        self.assertEqual(first_action.children[0].text, 'left')

    def test_second_action(self):
        second_action = self.rule.children[0].children[2].action_substitute
        self.assertIsInstance(second_action, nodes.RootAction)
        self.assertIsInstance(second_action.children[0], nodes.LiteralKeysAction)
        self.assertEqual(second_action.children[0].text, 'right')

class TestRuleSubstitute2(TestRuleParserBase):

    @classmethod
    def setUpClass(cls):
        cls.text = strings.SUBSTITUTE2

    def test_first_action(self):
        print(self.text)
        rule = self.rule