import unittest
from addons.Tests.UnitTests.data_containers_test.a_tools.auxilary_classes import random_BlackBox, comparable_BlackBox
from Modules.Settings.set_up_manager import SetUpManager

SetUpManager.SetUpRadarRecord()

class TestSaveToFile(unittest.TestCase):

    def test_1(self):
        filename = "data/saved_blackbox.txt"
        file = open(filename, "w")
        file.close()

        blackbox1 = random_BlackBox(2)
        blackbox1.SaveToFile(filename)

        blackbox2 = comparable_BlackBox()

        file = open(filename, "r")
        lines = file.readlines()
        blackbox2.LoadFromLines(lines)

        self.assertEqual(blackbox1, blackbox2)

if __name__ == '__main__':
    unittest.main()