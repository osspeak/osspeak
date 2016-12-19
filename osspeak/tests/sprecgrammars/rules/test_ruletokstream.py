import unittest

from sprecgrammars.rules import converter, parser, ruletokstream 
from sprecgrammars.rules.astree import GroupingNode, OrNode, WordNode 
from tests.sprecgrammars.rules import strings

class TestRuleParser(unittest.TestCase):

    def tokenize_rule(self, text):
        stream = ruletokstream.RuleTokenStream(text)
        return list(stream)

    def test_substitute1(self):
        tokens = self.tokenize_rule(strings.SUBSTITUTE1)
        self.assertEqual(len(tokens), 9)
        print(tokens, len(tokens))