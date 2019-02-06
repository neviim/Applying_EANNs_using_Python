import unittest
from addons.Tests.UnitTests.data_containers_test.a_tools.auxilary_classes import comparable_RecordOfRangefinder
from Modules.Simulation.geometry import Point
from Modules.Settings.set_up_manager import SetUpManager

SetUpManager.SetUpRadarRecord()

class TestLoadFromLine(unittest.TestCase):

    def test_1(self):
        ror1 = comparable_RecordOfRangefinder()
        ror1.pos = Point([2, 3])
        ror1.rot = 4
        ror1.posOfBarrier = Point([5, 6])

        ror2 = comparable_RecordOfRangefinder()
        ror2.LoadFromLine("2 3 4 5 6 ")

        self.assertEqual(ror1, ror2)

if __name__ == '__main__':
    unittest.main()