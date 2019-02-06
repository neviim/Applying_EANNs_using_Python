import unittest
from Modules.Simulation.data_containers import RangefinderRecord
from addons.Tests.UnitTests.data_containers_test.a_tools.auxilary_classes import comparable_RecordOfRadar
from Modules.Simulation.geometry import Point
from Modules.Settings.set_up_manager import SetUpManager

SetUpManager.SetUpRadarRecord()

class TestLoadFromLines(unittest.TestCase):

    def test_1(self):
        rorad1 = comparable_RecordOfRadar()
        rorad1.pos = Point([7, 8])
        rorad1.rot = 9

        for i in range(3):
            ror = RangefinderRecord()
            ror.LoadFromLine("2 3 4 5 6 ")
            rorad1.listOfRangefinderRecords[i] = ror

        rorad2 = comparable_RecordOfRadar()
        rorad2.LoadFromLines(["7 8 9",
                              "2 3 4 5 6 ",
                              "2 3 4 5 6 ",
                              "2 3 4 5 6 "])

        a=2

        self.assertEqual(rorad1, rorad2)


if __name__ == '__main__':
    unittest.main()