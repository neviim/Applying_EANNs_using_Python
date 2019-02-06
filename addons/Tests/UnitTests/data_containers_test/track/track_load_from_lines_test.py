import unittest
from Modules.Simulation.data_containers import RangefinderRecord, CarRecord, BlackBox
from addons.Tests.UnitTests.data_containers_test.a_tools.auxilary_classes import comparable_Track
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

        blackbox1 = BlackBox()
        for i in range(3):
            blackbox1.AddCarRecord(copy.deepcopy(roc1))
        blackbox2 = copy.deepcopy(blackbox1)

        track1 = comparable_Track()
        track1.AddBlackBox(blackbox1)
        track1.AddBlackBox(blackbox2)

        track2 = comparable_Track()
        track2.LoadFromLines(["5",
                              "3",
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
                              "2 3 4 5 6 ",
                              "3",
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

        self.assertTrue(track1 == track2)


if __name__ == '__main__':
    unittest.main()