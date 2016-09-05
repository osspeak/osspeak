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

    def test_basic_keypress(self):
        action = self.parse_action_string(strings.BASIC_KEYPRESS)
        self.assertEqual(len(action.children), 1)
        keypresses = action.children[0].keys
        self.assertTrue(all(isinstance(k, nodes.LiteralKeysAction) for k in keypresses))
        self.assertEqual([k.text for k in keypresses], ['shift', 'ctrl', 'e']) 

    def test_keypress_without_delimiter(self):
        with self.assertRaises(RuntimeError):
            action = self.parse_action_string(strings.KEYPRESS_WITHOUT_DELIMITER)