'''
TEST Segment:CalculateType(self):
'''
import unittest
from Modules.Simulation.geometry import Segment
from Modules.Simulation.geometry import Point

class TestCalculateType(unittest.TestCase):
    def test_normal(self):
        segment = Segment(Point(100, 200), Point(300, 400))
        self.assertEqual(segment.type.value, Segment.TypeOfSegment.NORMAL.value)

    def test_parallel_to_x(self):
        segment = Segment(Point(100, 400), Point(300, 400))
        self.assertEqual(segment.type.value, Segment.TypeOfSegment.PARALLEL_TO_X.value)

    def test_parallel_to_y(self):
        segment = Segment(Point(100, 200), Point(100, 400))
        self.assertEqual(segment.type.value, Segment.TypeOfSegment.PARALLEL_TO_Y.value)


if __name__ == '__main__':
    unittest.main()