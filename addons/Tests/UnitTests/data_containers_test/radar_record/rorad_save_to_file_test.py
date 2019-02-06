import unittest
from addons.Tests.UnitTests.data_containers_test.a_tools.auxilary_classes import random_RecordOfRadar, comparable_RecordOfRadar
from Modules.Settings.set_up_manager import SetUpManager

SetUpManager.SetUpRadarRecord()

class TestSaveToFile(unittest.TestCase):

    def test_1(self):
        filename = "data/saved_rorad.txt"
        file = open(filename, "w")
        file.close()

        rorad1 = random_RecordOfRadar()
        rorad1.SaveToFile(filename)

        rorad2 = comparable_RecordOfRadar()
        file = open(filename, "r")
        lines = file.readlines()

        rorad2.LoadFromLines(lines)

        self.assertTrue(rorad2 == rorad1)

        # self.assertEqual(rorad1, rorad2)


if __name__ == '__main__':
    unittest.main()