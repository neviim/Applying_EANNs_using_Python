import unittest
from Modules.Simulation.data_containers import RangefinderRecord, CarRecord
from addons.Tests.UnitTests.data_containers_test.a_tools.auxilary_classes import comparable_BlackBox
from Modules.Simulation.geometry import Point
import copy
from Modules.Settings.set_up_manager import SetUpManager

SetUpManager.SetUpRadarRecord()

class TestLoadFromLines(unittest.TestCase):

    def test_1(self):
        roc1 = CarRecord()
        roc1.pos = Point([10, 11])
        roc1.rot = 12
        roc1.radarRecord.pos = Point([7, 8])
        roc1.radarRecord.rot = 9

        for i in range(3):
            ror = RangefinderRecord()
            ror.LoadFromLine("2 3 4 5 6 ")
            roc1.radarRecord.listOfRangefinderRecords[i] = ror

        blackbox1 = comparable_BlackBox()
        for i in range(3):
            blackbox1.AddCarRecord(copy.deepcopy(roc1))

        blackbox2 = comparable_BlackBox()
        blackbox2.LoadFromLines(["3",
                                "10 11 12",
                                "7 8 9",
                                "2 3 4 5 6 ",
                                "2 3 4 5 6 ",
                                "2 3 4 5 6 ",
                                "10 11 12",
                                "7 8 9",
                                "2 3 4 5 6 ",
                                "2 3 4 5 6 ",
                                "2 3 4 5 6 ",
                                "10 11 12",
                                "7 8 9",
                                "2 3 4 5 6 ",
                                "2 3 4 5 6 ",
                                "2 3 4 5 6 "])

        a=2

        self.assertTrue(blackbox1 == blackbox2)


if __name__ == '__main__':
    unittest.main()