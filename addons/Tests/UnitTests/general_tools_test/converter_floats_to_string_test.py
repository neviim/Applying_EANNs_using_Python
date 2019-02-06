from Modules.General.general_tools import BuiltInTypesConverter
import unittest


class TestLineOfIntsFromList(unittest.TestCase):

    def test_1(self):
        list0 = [1.002, 23.00000000003, -0.009, 0, -4.0002, -3.999]
        self.assertEqual(BuiltInTypesConverter.FloatsToString(list0), "1.002 23.00000000003 -0.009 0 -4.0002 -3.999 ")


if __name__ == '__main__':
    unittest.main()