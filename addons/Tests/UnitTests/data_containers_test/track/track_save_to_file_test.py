import unittest
from addons.Tests.UnitTests.data_containers_test.a_tools.auxilary_classes import random_Track, comparable_Track
from Modules.Settings.set_up_manager import SetUpManager

SetUpManager.SetUpRadarRecord()

class TestSaveToFile(unittest.TestCase):

    def test_1(self):
        filename = "data/saved_track.txt"
        file = open(filename, "w")
        file.close()

        track1 = random_Track(2, 3)
        track1.SaveToFile(filename)

        track2 = comparable_Track()

        file = open(filename, "r")
        lines = file.readlines()
        track2.LoadFromLines(lines)

        self.assertEqual(track1, track2)

if __name__ == '__main__':
    unittest.main()