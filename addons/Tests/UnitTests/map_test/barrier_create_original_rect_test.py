'''
TEST - Barrier:CreateOriginalRect(self):
'''
import unittest
from Modules.Simulation.map import Barrier
from Modules.Simulation.geometry import Vector
from Modules.Settings.set_up_manager import SetUpManager

SetUpManager.SetUpPathsManager()
SetUpManager.SetUpImagesManager()
SetUpManager.SetUpBarrier()

class TestCreateOriginalRect(unittest.TestCase):

    def test_0(self):
        b1 = Barrier()
        b1.scale = Vector([2.1, 3.1])
        b1.CreateOriginalRect()
        self.assertEqual(b1.original_rect.bottomright, (67, 99))

if __name__ == '__main__':
    unittest.main()