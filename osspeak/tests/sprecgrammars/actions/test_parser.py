import unittest

from sprecgrammars.actions import nodes, tokens, parser
from tests.sprecgrammars.actions import strings

class TestActionParser(unittest.TestCase):

    def parse_action_string(self, action_string):
        action_parser = parser.ActionParser(action_string)
        action = action_parser.parse()
        self.assertIsInstance(action, nodes.RootAction)
        return action

    def test_empty(self):
        action = self.parse_action_string(strings.EMPTY)
        self.assertEqual(len(action.children), 0)