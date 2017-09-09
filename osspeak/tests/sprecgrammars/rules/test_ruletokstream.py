import unittest

from sprecgrammars.rules import converter, parser, ruletokstream, tokens
from sprecgrammars.rules.astree import GroupingNode, OrNode, WordNode 
from tests.sprecgrammars.rules import strings

class TestRuleTokenStreamBase(unittest.TestCase):

    @property
    def token_list(cls):
        stream = ruletokstream.RuleTokenStream(cls.text)
        print('stream', list(stream))
        return list(stream)

class TestRuleTokenStreamSubstitute(TestRuleTokenStreamBase):

    @classmethod
    def setUpClass(cls):
        cls.text = strings.SUBSTITUTE1

    def test_length(self):
        self.assertEqual(len(self.token_list), 9)

    def test_word_tokens(self):
        word_tokens = [tok.text for tok in self.token_list if isinstance(tok, tokens.WordToken)]
        self.assertEqual(word_tokens, ['west', 'east'])

    def test_action_substitutes(self):
        actions = [tok.action for tok in self.token_list if isinstance(tok, tokens.ActionSubstituteToken)]
        self.assertEqual([a.children[0].text for a in actions], ['left', 'right'])