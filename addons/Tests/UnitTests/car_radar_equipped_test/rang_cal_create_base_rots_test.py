'''
TEST RangefinderTransformCalculator:CreateListOfBaseRots(cls, numberOfRangefinders, range1):
'''
from Modules.Simulation.car_radar_equipped import RangefinderTransformCalculator
import unittest


class TestRangefinderTransformCalculator(unittest.TestCase):
    def test_CreateBaseRots(self):
        RangefinderTransformCalculator.CalculateRelativeRots(60, 4)
        self.assertTrue(RangefinderTransformCalculator.listOfRelativeRots == [-30.0, -10.0, 10.0, 30.0])

if __name__ == '__main__':
    unittest.main()

