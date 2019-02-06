'''
Author: Pawel Brysch
Date: Jan 2019

This script allow you perform experiments and save all necessary data about them.

To use this script you can manipulate its code in 4 places:
1) set number of first experiment at the beginning of the script.
2) change parameters which are saved by "AddSummaryToRegistry" method (inside "SolutionFinder" class)
3) change parameters of experiment (at the end of this script)
4) set how many experiments will be performed (at the end of the script)

Because we have freedom in performing experiment, you should treat points 3) and 4) elastically. It means that you can
change parameters which you want after each experiment.
'''

from Modules.AI.Genetics.genetics import AlbumWriter, EvolutonaryAlgorithm
from Modules.General.general_tools import PathsManager
from Modules.Settings.settings import SETTINGS
from Modules.Settings.set_up_manager import SetUpManager

# Set number of first experiment.
numberOfFirstExperiment = 512

class SolutionFinder:
    ''' Class consist of method, which allow you to perform experiment and simple counter.
        It allows you to perform many experiments in one execution.

    ...
    Attributes
    ----------
    numberOfExperiment: int
        number of experiment which are performing at given moment.
    '''
    # Notice: "numberOfExperiment" will be incremented for next experiments in the same script.
    numberOfExperiment = numberOfFirstExperiment

    @classmethod
    def PerformExperiment(cls, poolNumber = None):
        ''' Perform single experiment and save all possible results (album, gene pool of last population and summary with
        best and average fitnesses (other parameters are optional)

        :param poolNumber: int
            Set, if you want to start your experiment not from the random beginning, but from the saved progress.
        '''

        # Set up environment
        SetUpManager.SetUp()

        # Load population if experiment doesn't start from the random beginning.
        if poolNumber is not None:
            EvolutonaryAlgorithm.LoadPopulation("data/genePools/pool" + str(poolNumber) + ".txt")

        # Perform experiment
        EvolutonaryAlgorithm.Execute()

        # Create album
        album = AlbumWriter.AlbumFromAlgorithm(EvolutonaryAlgorithm)

        # Save results
        cls.SaveAlbum(album)
        cls.SaveGenePool()
        cls.AddSummaryToRegistry()

        # Increment counter (next experiment will have another number)
        cls.numberOfExperiment += 1

    @classmethod
    def SaveAlbum(cls, album):
        ''' Save album. In other words, the course of experiment, step by step.
        '''
        album.SaveToFile(PathsManager.GetPath("albums", "album" + str(cls.numberOfExperiment) + ".txt"))

    @classmethod
    def SaveGenePool(cls):
        ''' Save genes of all individuals from the last population.
        '''
        EvolutonaryAlgorithm.SavePopulation(PathsManager.mainPath + "Scripts/Data/genePools/pool" + str(cls.numberOfExperiment) + ".txt")


    @classmethod
    def AddSummaryToRegistry(cls):
        ''' Add summary (one line) about performed experiment to file "registry.txt:, which contains information about
        all performed experiments.
        '''
        with open(PathsManager.mainPath + "Scripts/data/registry.txt", "a") as file:

            # Write number of experiment.
            file.write("album no: " + str(cls.numberOfExperiment) + " ")

            # Write optional information. Typically, parameters which are tuned at this time.
            # Here is an example:
            # file.write("after" + str(SETTINGS.GENETICS.SIZE_OF_POPULATION_AFTER_SELECTION) + " ")
            # file.write("before" + str(SETTINGS.GENETICS.SIZE_OF_POPULATION_BEFORE_SELECTION) + " ")

            # Write average and best fitnesse.
            file.write("avg" + str(EvolutonaryAlgorithm.logbook.select("avg")[-1]) + " ")
            file.write("best" + str(EvolutonaryAlgorithm.logbook.select("max")[-1]) + "\n")

            file.close()

# At this place you can change parameters of experiment, which are in "Settings" module by default.
SETTINGS.GENETICS.CROSSING.PROBABILITY = 0.5
SETTINGS.GENETICS.MUTATION.PROBABILITY = 0.2

SETTINGS.GENETICS.SIZE_OF_POPULATION_AFTER_SELECTION = 30
SETTINGS.GENETICS.SIZE_OF_POPULATION_BEFORE_SELECTION = 60
SETTINGS.GENETICS.NUMBER_OF_GENERATIONS = 10

# Perform experiment as many times as you want by using line below multiple times.
SolutionFinder.PerformExperiment()


