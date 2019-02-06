from Modules.General.general_tools import BuiltInTypesConverter
import unittest


class TestLineOfIntsFromList(unittest.TestCase):

    def test_1(self):
        list0 = [100, 23.03, 435, 0, -4, -3.999]
        self.assertEqual(BuiltInTypesConverter.IntsToString(list0), "100 23 435 0 -4 -3 ")



if __name__ == '__main__':
    unittest.main()