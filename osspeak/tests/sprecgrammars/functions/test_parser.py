import os
import unittest

from sprecgrammars.functions import astree, tokens, parser
from tests.sprecgrammars.functions import strings

class TestFunctionParser(unittest.TestCase):

    def parse_function_string(self, function_string):
        function_parser = parser.FunctionDefinitionParser(function_string)
        func = function_parser.parse()
        self.assertIsInstance(func, astree.FunctionDefinition)
        return func

    def test_no_params(self):
        func = self.parse_function_string(strings.NO_PARAMS)
        self.assertEqual(func.name, 'foo')
        self.assertEqual(func.parameters, [])

    def test_positional_params(self):
        func = self.parse_function_string(strings.POSITIONAL_PARAMS)
        self.assertEqual(func.name, 'funcName')
        self.assertEqual(len(func.parameters), 2)
        self.assertIsInstance(func.parameters[0], astree.FunctionParameter)
        self.assertIsInstance(func.parameters[1], astree.FunctionParameter)
        self.assertEqual(func.parameters[0].name, 'bar')
        self.assertEqual(func.parameters[1].name, 'baz')
        
        

    # def test_basic_keypress(self):
    #     action = self.parse_function_string(strings.BASIC_KEYPRESS)
    #     self.assertEqual(len(action.children), 1)
    #     keypresses = action.children[0].keys
    #     self.assertTrue(all(isinstance(k, nodes.LiteralKeysAction) for k in keypresses))
    #     self.assertEqual([k.text for k in keypresses], ['shift', 'ctrl', 'e']) 

    # def test_keypress_without_delimiter(self):
    #     with self.assertRaises(RuntimeError):
    #         action = self.parse_function_string(strings.KEYPRESS_WITHOUT_DELIMITER)

    # def test_basic_function(self):
    #     action = self.parse_function_string(strings.BASIC_FUNCTION)
    #     self.assertEqual(len(action.children), 1)
    #     self.assertIsInstance(action.children[0], nodes.FunctionCall)
    #     self.assertEqual(action.children[0].func_name, 'mouse.click')
    #     self.assertEqual(action.children[0].arguments, [])