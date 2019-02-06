from Modules.AI.Genetics.genetics import EvolutonaryAlgorithm
from Modules.Settings.set_up_manager import SetUpManager
import unittest


def EvaluatePattern(gaPattern):
    return sum(gaPattern),

# #SETUP
SetUpManager.SetUp()

EvolutonaryAlgorithm.Prepare()
EvolutonaryAlgorithm.toolbox.register("evaluate", EvaluatePattern)
EvolutonaryAlgorithm.Execute()

class TestPatternBreeder(unittest.TestCase):
    def test_effect(self):
        self.assertTrue(max(EvolutonaryAlgorithm.logbook.select("max")) > 15)
        self.assertTrue(max(EvolutonaryAlgorithm.logbook.select("avg")) > 15)

if __name__ == '__main__':
    unittest.main()