'''
TEST Ray:CalculateBaseVector(self):
'''
import unittest
from Modules.Simulation.geometry import Ray
from Modules.Simulation.geometry import Point

def func1(vec):
    return [vec.x, vec.y]


class TestCalculateExtrema(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(func1(Ray(Point([50, 50]), Point([100, 100])).baseVector), [1, 1])
        self.assertEqual(func1(Ray(Point([50, 50]), Point([-50, 100])).baseVector), [-1, 1])
        self.assertEqual(func1(Ray(Point([50, 50]), Point([100, -50])).baseVector), [1, -1])
        self.assertEqual(func1(Ray(Point([50, 50]), Point([-50, -50])).baseVector), [-1, -1])
        self.assertEqual(func1(Ray(Point([50, 50]), Point([50, 100])).baseVector), [0, 1])
        self.assertEqual(func1(Ray(Point([50, 50]), Point([100, 50])).baseVector), [1, 0])
        self.assertEqual(func1(Ray(Point([50, 50]), Point([50, -50])).baseVector), [0, -1])
        self.assertEqual(func1(Ray(Point([50, 50]), Point([-50, 50])).baseVector), [-1, 0])


if __name__ == '__main__':
    unittest.main()