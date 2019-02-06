import unittest
from Modules.Simulation.data_containers import RangefinderRecord, RadarRecord
from addons.Tests.UnitTests.data_containers_test.a_tools.auxilary_classes import comparable_RecordOfCar
from Modules.Simulation.geometry import Point
from Modules.Settings.set_up_manager import SetUpManager

SetUpManager.SetUpRadarRecord()

class TestLoadFromLines(unittest.TestCase):

    def test_1(self):
        roc1 = comparable_RecordOfCar()
        roc1.pos = Point([10, 11])
        roc1.rot = 12
        # roc1.recordOfRadar = RadarRecord()
        roc1.radarRecord.pos = Point([7, 8])
        roc1.radarRecord.rot = 9

        for i in range(3):
            ror = RangefinderRecord()
            ror.LoadFromLine("2 3 4 5 6 ")
            roc1.radarRecord.listOfRangefinderRecords[i] = ror

        roc2 = comparable_RecordOfCar()
        roc2.radarRecord = RadarRecord()

        roc2.LoadFromLines(["10 11 12",
                              "7 8 9",
                              "2 3 4 5 6 ",
                              "2 3 4 5 6 ",
                              "2 3 4 5 6 "])

        self.assertEqual(roc1, roc2)


if __name__ == '__main__':
    unittest.main()