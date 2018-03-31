import os
import unittest

from recognition.actions import asttransform
from tests.recognition.actions import strings

class TestAstTransform(unittest.TestCase):

    def evaluate(self, expr_text, usrglobals=None, usrlocals=None):
        usrglobals, usrlocals = usrglobals or globals(), usrlocals or locals()
        expr = asttransform.transform_expression(expr_text)
        return eval(expr, usrglobals, usrlocals)

    def test_lambda(self):
        res = self.evaluate(strings.LAMBDA_EXPRESSION)
        self.assertEqual(res, 9)

    def test_kwarg(self):
        res = self.evaluate(strings.KWARG_EXPRESSION)
        self.assertEqual(res, 45)

    def test_sorted(self):
        res = self.evaluate(strings.SORTED_EXPR)
        self.assertEqual(res, [2, 3, 4])

    def test_top_level_builtin(self):
        res = self.evaluate(strings.TOP_LEVEL_BUILTIN)
        self.assertEqual(res, 'len')

    def test_index(self):
        res = self.evaluate(strings.INDEX_EXPR, usrlocals={'x': [5]})
        self.assertEqual(res, 5)
