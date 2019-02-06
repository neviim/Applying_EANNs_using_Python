'''
TEST Pattern:RevaluateLength(cls, architecture):
'''
from Modules.AI.Genetics.genetics import Pattern
import unittest

class TestCalculateLength(unittest.TestCase):

    def test_appropriate_length(self):
        Pattern.CalculateLength([3, 4, 3, 2])
        self.assertEqual(Pattern.length, 39)

    def test_length_two(self):
        Pattern.CalculateLength([3, 5, 2])
        self.assertEqual(Pattern.length, 32)

if __name__ == '__main__':
    unittest.main()