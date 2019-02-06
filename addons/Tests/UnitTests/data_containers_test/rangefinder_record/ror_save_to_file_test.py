import unittest
from addons.Tests.UnitTests.data_containers_test.a_tools.auxilary_classes import random_RecordOfRangefinder, comparable_RecordOfRangefinder
from Modules.Settings.set_up_manager import SetUpManager

SetUpManager.SetUpRadarRecord()

class TestSaveToFile(unittest.TestCase):

    def test_1(self):
        filename = "data/saved_ror.txt"
        file = open(filename, "w")
        file.close()

        ror1 = random_RecordOfRangefinder()
        ror1.SaveToFile(filename)

        ror2 = comparable_RecordOfRangefinder()
        file = open(filename, "r")
        line = file.readlines()[0]
        ror2.LoadFromLine(line)

        self.assertEqual(ror1, ror2)

        file.close()


if __name__ == '__main__':
    unittest.main()