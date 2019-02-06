'''
TEST-II ProjectionCalculator::PointOfLineBelongsToRay(cls, point, ray):
'''
from Modules.Simulation.geometry import Point, Ray
import unittest


class TestBelongsCollinearPoint(unittest.TestCase):

    def test_first_quarter(self):
        ray = Ray(Point(20,70), Point(40,80))
        point1 = Point((51, 86))
        point2 = Point((14, 67))

        self.assertTrue(ray.BelongsCollinearPoint(point1))
        self.assertFalse(ray.BelongsCollinearPoint(point2))

    def test_second_quarter(self):
        ray = Ray(Point(30,50), Point(10,60))
        point1 = Point((16, 57))
        point2 = Point((50, 40))

        self.assertTrue(ray.BelongsCollinearPoint(point1))
        self.assertFalse(ray.BelongsCollinearPoint(point2))

    def test_third_quarter(self):
        ray = Ray(Point(30,40), Point(10,30))
        point1 = Point((2, 26))
        point2 = Point((50, 51))

        self.assertTrue(ray.BelongsCollinearPoint(point1))
        self.assertFalse(ray.BelongsCollinearPoint(point2))

    def test_fourth_quarter(self):
        ray = Ray(Point(30,20), Point(50,10))
        point1 = Point((56, 7))
        point2 = Point((23, 24))

        self.assertTrue(ray.BelongsCollinearPoint(point1))
        self.assertFalse(ray.BelongsCollinearPoint(point2))

    def test_parallel_to_x_plus(self):
        ray = Ray(Point(80,80), Point(100,80))
        point1 = Point((113, 80))
        point2 = Point((68, 70))

        self.assertTrue(ray.BelongsCollinearPoint(point1))
        self.assertFalse(ray.BelongsCollinearPoint(point2))

    def test_parallel_to_x_minus(self):
        ray = Ray(Point(90,70), Point(70,70))
        point1 = Point((58, 70))
        point2 = Point((106, 70))

        self.assertTrue(ray.BelongsCollinearPoint(point1))
        self.assertFalse(ray.BelongsCollinearPoint(point2))

    def test_parallel_to_y_plus(self):
        ray = Ray(Point(90,30), Point(90,50))
        point1 = Point((90, 45))
        point2 = Point((90, 21))

        self.assertTrue(ray.BelongsCollinearPoint(point1))
        self.assertFalse(ray.BelongsCollinearPoint(point2))

    def test_parallel_to_y_minus(self):
        ray = Ray(Point(110,40), Point(110,20))
        point1 = Point((110, 15))
        point2 = Point((110, 53))

        self.assertTrue(ray.BelongsCollinearPoint(point1))
        self.assertFalse(ray.BelongsCollinearPoint(point2))


if __name__ == '__main__':
    unittest.main()