import os
import unittest

from sprecgrammars.actions import nodes, tokens, parser
from sprecgrammars import api
from tests.sprecgrammars.actions import strings

class TestActionParser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.function_definitions = {}
        defs = {
            'mouse.click()': '' 
        }
        for sig, action in defs.items():
            func_def = api.func_definition(sig, action)
            cls.function_definitions[func_def.name] = func_def

    def parse_action_string(self, action_string):
        action = api.action(action_string, self.function_definitions)
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

    def test_basic_function(self):
        action = self.parse_action_string(strings.BASIC_FUNCTION)
        self.assertEqual(len(action.children), 1)
        self.assertIsInstance(action.children[0], nodes.FunctionCall)
        self.assertEqual(action.children[0].func_name, 'mouse.click')
        self.assertEqual(action.children[0].arguments, [])

    def test_extensions_function(self):
        action = self.parse_action_string(strings.EXTENSIONS_FUNCTION)

    def test_extensions_args_function(self):
        action = self.parse_action_string(strings.EXTENSIONS_FUNCTION_WITH_ARGS)
        print(action)
        