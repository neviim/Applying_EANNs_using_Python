from Modules.Simulation.geometry import Vector
import unittest


class TestAngleOfVec(unittest.TestCase):

    def test_0(self):
        self.assertEqual(Vector(20,34).angle, 301)

if __name__ == '__main__':
    unittest.main()