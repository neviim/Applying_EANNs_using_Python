import unittest
from Modules.General.general_tools import BuiltInTypesConverter


class TestListOfIntsFromLine(unittest.TestCase):

    def test_1(self):
        line = "122 123 124"
        self.assertEqual(BuiltInTypesConverter.StringToInts(line), [122, 123, 124])


if __name__ == '__main__':
    unittest.main()