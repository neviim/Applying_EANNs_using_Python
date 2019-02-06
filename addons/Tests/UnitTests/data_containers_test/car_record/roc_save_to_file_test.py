import unittest
from addons.Tests.UnitTests.data_containers_test.a_tools.auxilary_classes import random_RecordOfCar, comparable_RecordOfCar
from Modules.Settings.set_up_manager import SetUpManager

SetUpManager.SetUpRadarRecord()

class TestSaveToFile(unittest.TestCase):

    def test_1(self):
        filename = "data/saved_roc.txt"
        file = open(filename, "w")
        file.close()

        roc1 = random_RecordOfCar()
        roc1.SaveToFile(filename)

        roc2 = comparable_RecordOfCar()
        file = open(filename, "r")
        lines = file.readlines()
        roc2.LoadFromLines(lines)

        self.assertEqual(roc1, roc2)

if __name__ == '__main__':
    unittest.main()