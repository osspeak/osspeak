import os
import unittest

from recognition.commands import match
from recognition import api
from tests.recognition.actions import strings

class TestAstTransform(unittest.TestCase):

    def test_count_repetition(self):
        self.assertEqual(match.count_repetition(['alpha', 'alpha', 'alpha', 'bravo', 'charlie'], 1), 2)

    def test_count_repetition_non_repeating(self):
        self.assertEqual(match.count_repetition(['this', 'is', 'a', 'test'], 0), 1)