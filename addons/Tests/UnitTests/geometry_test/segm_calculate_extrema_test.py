'''
TEST Segment:CalculateExtrema(self):
'''
import unittest
from Modules.Simulation.geometry import Segment
from Modules.Simulation.geometry import Point

class TestCalculateExtrema(unittest.TestCase):
    def test_normal(self):
        segment = Segment(Point((100, 20)), Point((40, 80)))
        self.assertEqual(segment.min_x, 40)
        self.assertEqual(segment.max_x, 100)
        self.assertEqual(segment.min_y, 20)
        self.assertEqual(segment.max_y, 80)


if __name__ == '__main__':
    unittest.main()