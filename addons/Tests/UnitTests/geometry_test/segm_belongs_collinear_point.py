'''
TEST Segment::BelongsCollinearPoint(self, point):
'''
# from pos_of_barrier_calculator import ProjectionCalculator
from Modules.Simulation.geometry import Point, Segment
import unittest


class TestBelongsCollinearPoint(unittest.TestCase):

    def test_normal(self):
        segment = Segment( Point(100,50), Point(250,100) )
        point1 = Point((200, 83))
        point2 = Point((50, 33))
        point3 = Point((300, 117))

        self.assertTrue(segment.BelongsCollinearPoint(point1))
        self.assertFalse(segment.BelongsCollinearPoint(point2))
        self.assertFalse(segment.BelongsCollinearPoint(point3))


    def test_nearly_parallel(self):
        segment = Segment( Point(991,49), Point(992,377) )
        point1 = Point((992, 456))

        self.assertFalse(segment.BelongsCollinearPoint(point1))

    def test_parallel_to_x(self):
        segment = Segment(Point(100, 200), Point(300, 200))
        point1 = Point((200, 200))
        point2 = Point((50, 200))
        point3 = Point((350, 200))

        self.assertTrue(segment.BelongsCollinearPoint(point1))
        self.assertFalse(segment.BelongsCollinearPoint(point2))
        self.assertFalse(segment.BelongsCollinearPoint(point3))

    def test_parallel_to_y(self):
        segment = Segment(Point(200,400), Point(200,600))
        point1 = Point((200, 500))
        point2 = Point((200, 200))
        point3 = Point((200, 700))

        self.assertTrue(segment.BelongsCollinearPoint(point1))
        self.assertFalse(segment.BelongsCollinearPoint(point2))
        self.assertFalse(segment.BelongsCollinearPoint(point3))

if __name__ == '__main__':
    unittest.main()