import unittest
from addons.Tests.UnitTests.data_containers_test.a_tools.auxilary_classes import random_Album, comparable_Album
from Modules.Settings.set_up_manager import SetUpManager

'''
w innych tez to dodac
'''
SetUpManager.SetUpRadarRecord()

class TestSaveToFile(unittest.TestCase):

    def test_1(self):
        filename = "data/saved_album.txt"
        file = open(filename, "w")
        file.close()

        album1 = random_Album(3, 2, 3)
        album1.SaveToFile(filename)

        album2 = comparable_Album()

        file = open(filename, "r")
        lines = file.readlines()
        album2.LoadFromLines(lines)


        self.assertEqual(album1, album2)

if __name__ == '__main__':
    unittest.main()