''' GENETICS
Author: Pawel Brysch
Date: Jan 2019

Module contains classes which together allow perform simulation of evolution.

...
Classes
----------
Pattern:
    This is a genotype in our algorithm.
FitnessEvaluator:
    This class connects algorithm with simulation environment.
EvolutionaryAlgorithm:
    Proper genetic algorithm
AlbumWriter:
    This class writes album by getting data from algorithm.
'''

from Modules.General.general_tools import BuiltInTypesConverter, FilesManager
from Modules.Simulation.data_containers import Album, Track, BlackBox
from deap import base, creator, tools
from deap.algorithms import varOr
import random
import copy




class Pattern(list):
    ''' Genotype. It is used only when phenotype is neural network.

    ...
    Attributes
    ----------
    length: int
        class attribute. It represents number of genes.
    wageMin: float
        class attribute. Minimal value of gen.
    wageMax: float
        class attribute. Maximal value of gen.

    fitness: deap.base.Fitness
        object is required by the DEAP framework. It also contains "fitness" in typical meaning.
    blackBox: BlackBox
        it works as pointer.
        In simulation is only one car, which changes patterns. Hence proper place to store data about drive is just
        pattern. It works as pointer to copy of black box which was temporarily created in car object during single drive.
    '''
    length = None

    wageMin = None
    wageMax = None

    def __init__(self, *args):
        list.__init__(self, *args)
        self.fitness = creator.FitnessMax()
        self.blackBox = BlackBox()

    @property
    def wages(self):
        return self

    @classmethod
    def RandomWage(cls):
        ''' Method returns random wage. In our case we use simple method from "random" library.

        :return: float
        '''

        return random.uniform(cls.wageMin, cls.wageMax)

    @classmethod
    def CalculateLength(cls, architecture):
        ''' Method calculates number of genes in genotype.

        :param architecture: list
            list of numbers of neurons in consecutive layers in neural network
        :return:
            number of connections in neural network (biases included)
        '''
        result = 0

        # To understand how lines written below works you need to understand how neural networks are constructed.
        # After that, it is easy mathematical exercise to determine number of connections depending on architecture
        # (number of layers, number of neurons per each layer).
        for index in range(len(architecture)-1):
            result += architecture[index] * architecture[index+1]

        result += sum(architecture)
        result -= architecture[0]

        cls.length = result



class FitnessEvaluator:
    ''' This class connects algorithm with simulation environment. Simplifying it is just method which we use to
    evaluate fitness of pattern. The reason why we use a separate class is that the DEAP was designed to use evaluation
    methods, which only evaluate. In addition we have to provide some way to store data about drives.
    So we have this class.

    ...
    Attributes
    ----------
    verbose: bool
        if equals True, it prints fitnesses of consecutive cars. It helps recognize whether experiment is going in the
        right direction during experiment, even at the beginning.
    car: TrainableCar
        we use just single car for all experiments. This is due the fact that we choose "render-before, display-after"
        style of performing experiment instead of "real-time"
    '''
    verbose = False
    car = None

    @classmethod
    def EvaluatePattern(cls, pattern):
        ''' The evaluation method used in our genetic algorithm.

        :param pattern: Pattern
            pattern which will be evaluated
        :return: int
            fitness of pattern
        '''
        # Set pattern (individual) on object that will allow to measure fitness.
        cls.car.brain.SetPattern(pattern)

        # Proper simulation.
        cls.car.PerformDrive()

        # Copy record of drive. REMEMBER: there are many patterns and only one car, so we have to do that.
        pattern.blackBox = cls.car.blackBox

        # See: "verbose" description in class documentation.
        if cls.verbose:
            print("next", cls.car.stepCounter)

        return copy.deepcopy(cls.car.stepCounter),



class EvolutonaryAlgorithm:
    ''' Interface thanks to which you can use DEAP framework. It connects all features in one class.

        IMPORTANT!
        Barely all of attributes have to be set in external module (e.q. settings).
    ...
    Attributes
    ----------
    startFromRandomPopulation: bool
        whether algorithm starts from drawing random genotypes. The alternative is to load population from previous
        experiment.
    startingPopulation: list
        list of individuals. By default it is created automatically.
    toolbox: base.Toolbox()
        core object of DEAP framework. It is used multiple time in class's implementation.
    lverbose: bool
        if True, it prints number of currently evaluated generation

    #INDIVIDUALS
    lengthOfIndividual: int
        how many genes individual has.
    geneRandomizingFunction:
        method which returns random gene if we use it.

    #LAWS
    fitnessEvaluator: FitnessEvaluator
        see: "FitnessEvaluator" class description.

    probabilityOfCrossing: float
    crossingMethod: method
        By default one of DEAP's crossing methods. If you want to create your own it has to have similar implementation
        (input especially).
    crossingParameters: dict
        packed additional arguments required by chosen method.

    probabilityOfMutation: float
    mutationMethod: method
        By default one of DEAP's mutation methods. If you want to create your own it has to have similar implementation
        (input especially).
    mutationParameters: dict
        packed additional arguments required by chosen method.

    selectionMethod: method
        By default one of DEAP's selection methods. If you want to create your own it has to have similar implementation
        (input especially).
    selectionParameters: dict
        packed additional arguments required by chosen method.

    #MAKRO
    paramMu: int
        number of individuals in population after selection. Also number of individuals in starting population.
    paramLambda: int
        number of individuals in population before selection.
    numberOfGenerations: int


    #STATISTICS
    stats: tools.Statistics
        DEAP's tool which is used many times during work of algorithm.
    dictWithStatistics: dict
        It should have format dict((str, method)), where "str" - name of chosen method. MEthod must allow it to be used
        on set of arguments.


    #RESULTS
    listOfPopulations: list
        every element from the list is population from one generation from experiment.
    logbook: tools.Logbook
        data container for statistics. Could be accessed if you want to make some graphs related to statistics.
    finalPopulation: list
        population of last generation from the experiment.
    '''
    startFromRandomPopulation = True
    startingPopulation = None

    toolbox = base.Toolbox()
    lverbose = False

    #INDIVIDUALS
    lengthOfIndividual = None
    geneRandomizingFunction = None

    #LAWS
    fitnessEvaluator = FitnessEvaluator

    probabilityOfCrossing = None
    crossingMethod = None
    crossingParameters = {}

    probabilityOfMutation = None
    mutationMethod = None
    mutationParameters = {}

    selectionMethod = None
    selectionParameters = {}

    #MAKRO
    paramMu = None
    paramLambda = None
    numberOfGenerations = None


    #STATISTICS
    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    dictWithStatistics = {}

    #RESULTS
    listOfPopulations = None
    logbook = None
    finalPopulation = None

    @classmethod
    def Prepare(cls):
        ''' Prepare algorithm to future work.
            It is necessary to use this method before simulation.
            Take care if every attributes was properly assigned.
            After using this method you can use algorithm many times in one execution.
        '''

        # Set method which will choose genes.
        cls.toolbox.register("attr_float", cls.geneRandomizingFunction)

        # A necessary line that we would be able to create individuals
        cls.toolbox.register("individual", tools.initRepeat, Pattern, cls.toolbox.attr_float, n=cls.lengthOfIndividual)

        # A necessary line that we would be able to create populations.
        cls.toolbox.register("population", tools.initRepeat, list, cls.toolbox.individual)

        # Create methods which will be used during algorithm.
        cls.toolbox.register("evaluate", cls.fitnessEvaluator.EvaluatePattern)
        cls.toolbox.register("mate", cls.crossingMethod, **cls.crossingParameters)
        cls.toolbox.register("mutate", cls.mutationMethod, **cls.mutationParameters)
        cls.toolbox.register("select", cls.selectionMethod, **cls.selectionParameters)

        # Create set of statistics.
        for name, method in cls.dictWithStatistics.items():
            cls.stats.register(name, method)

    @classmethod
    def LoadPopulation(cls, filename):
        ''' Load final population from previous experiment and set it as starting population.
            Be aware that every line in file contains saved wages of one individual.
        '''

        lines = FilesManager.LinesFromFile(filename)
        cls.startingPopulation = cls.toolbox.population(len(lines))
        for individual, line in zip(cls.startingPopulation, lines):
            importedWages = BuiltInTypesConverter.StringToFloats(line)
            for _ in range(len(individual)):
                # Remember that "Pattern" derives from "list", so we need to use old-fashioned style.
                individual.wages[_] = importedWages[_]

        # Starting population won't be randomly generated.
        cls.startFromRandomPopulation = False


    @classmethod
    def SavePopulation(cls, filename):
        ''' Save final population for future purposes
            Be aware that every line in file contains saved wages of one individual.
        '''

        FilesManager.ClearFile(filename)

        for individual in cls.finalPopulation:
            nextLine = BuiltInTypesConverter.FloatsToString(individual.wages)
            FilesManager.AddLineToFile(nextLine, filename)


    @classmethod
    def Execute(cls):
        ''' By default we use comma-selection version of algorithm.  There exist also other versions (e.q.
            plus-selection). It is place, which potentially allows to switch between different versions.
        '''

        # Creates randomly generated population, if none has been loaded.
        if cls.startFromRandomPopulation:
            cls.startingPopulation = cls.toolbox.population(cls.paramMu)

        # The core of algorithm
        cls.eaMuCommaLambda(population=cls.startingPopulation,
                            toolbox=cls.toolbox,
                            mu=cls.paramMu,
                            lambda_=cls.paramLambda,
                            cxpb=cls.probabilityOfCrossing,
                            mutpb=cls.probabilityOfMutation,
                            ngen=cls.numberOfGenerations,
                            stats=cls.stats)

        # Reset flag for next execution.
        cls.startFromRandomPopulation = True

    @classmethod
    def eaMuCommaLambda(cls, population, toolbox, mu, lambda_, cxpb, mutpb, ngen, stats=None):
        ''' Method has been copied from DEAP framework in order to add some additional features (like adding verbosity
            and a method which collect additional data related with simulations).

            If you want to understand meaning of arguments please see usage of this method in "Execute" and read about
            algorithm attributes in class description.
        '''

        assert lambda_ >= mu, "lambda must be greater or equal to mu."

        # Create new logbook
        cls.logbook = tools.Logbook()
        cls.logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the statistics with the new population
        record = stats.compile(population) if stats is not None else {}
        cls.logbook.record(gen=0, nevals=len(invalid_ind), **record)

        cls.listOfPopulations = []
        cls.listOfPopulations.append(copy.deepcopy(population))

        # Begin the generational process
        for gen in range(1, ngen + 1):
            if cls.lverbose:
                print("generation no:", gen)

            # Vary the population
            offspring = varOr(population, toolbox, lambda_, cxpb, mutpb)

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # Select the next generation population
            population[:] = toolbox.select(offspring, mu)

            # Update the statistics with the new population
            record = stats.compile(population) if stats is not None else {}
            cls.logbook.record(gen=gen, nevals=len(invalid_ind), **record)

            cls.listOfPopulations.append(copy.deepcopy(population))

        # Get final population
        cls.finalPopulation = population


class AlbumWriter:
    ''' One-method class which can write album by getting data from algorithm.
        Connects algorithmic part of program with GUI.
    '''
    @classmethod
    def AlbumFromAlgorithm(cls, algorithm):
        ''' Write album by getting data from algorithm.
        :param algorithm: EvolutionaryAlgorithm
        :return: Album
        '''
        album = Album()

        for population in algorithm.listOfPopulations:
            track = Track()
            for pattern in population:
                track.AddBlackBox(pattern.blackBox)
            album.AddTrack(track)

        return album


