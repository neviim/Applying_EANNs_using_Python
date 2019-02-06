'''
TEST Point::Distance(self, point):
'''
from Modules.Simulation.geometry import Point
import unittest

class TestDistance(unittest.TestCase):

    def test_only(self):
        self.assertEqual(Point([2, 3]).Distance(Point([5, 7])), 5)
        self.assertEqual(Point([0, 0]).Distance(Point([10, 5])), 11)

if __name__ == '__main__':
    unittest.main()
