''' SETUP MANAGER
Author: Pawel Brysch
Date: Jan 2019

Module contains "SetUpManager" class, which is core of all project.
'''

from Modules.Settings.settings import SETTINGS

from Modules.AI.Genetics.genetics import Pattern, FitnessEvaluator, EvolutonaryAlgorithm
from Modules.AI.NeuralNetworks.neural_networks import InputTransformator, OutputTransformator, Brain
from Modules.GUI.displayer import CarRelatedSpritesContainer, Camera, Displayer
from Modules.GUI.sprites import SSmallSquare, SRangefinder, SRadar, SBarrier, SCar
from Modules.Simulation.data_containers import RadarRecord
from Modules.Simulation.car_base import CarTransformCalculator, BaseCar
from Modules.Simulation.car_radar_equipped import RangefinderTransformCalculator, RadarTransformCalculator, Radar
from Modules.Simulation.car_trainable import TrainableCar
from Modules.General.general_tools import ImagesManager, PathsManager
from Modules.Simulation.geometry import Vector, ProjectionCalculator
from Modules.Simulation.map import Map, Barrier

from deap import creator, base
import pygame as pg
import os




class SetUpManager:
    '''
        Prepare all classes in project to be usable. For this purpose this class:
        - set all class attributes
        - execute all necessary classmethods which has to be executed before the the main work of each class.

        If you created a class you need to add "method" for this class to SetUpManager.

        # HOW TO ADD CLASS
        Lets assume that we class named "Bar" which need class "Casino" to be set before it.
        "method" should have format:

        @classmethod
        def SetUpBar(cls):
            cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpCasino)
            ...
            set class variables (from Bar class)
            ...
            use classmethods (from Bar class)

        # HOW TO USE IN SCRIPTS/TESTS
        You can use this class in two ways:
        1) Use "SetUp" method at the beginning of the script.
        2) Use chosen "methods" at the beginning of the script. Use in case when you need to set up only few classes for
        the script to work well.


    ...
    Attributes
    ----------
    methodToBool: dict
        :key - "method"
        :value - if "method" was executed or not
    '''
    methodToBool = {}


    @classmethod
    def SetUp(cls):
        ''' Use at the beginning of script if you want to set up all "methods".
            See: "method" in class description
        '''

        # Set all "methods" unexecuted.
        cls.Reset()

        # Execute all "methods"
        cls.ExecuteAllMethods()

    @classmethod
    def Reset(cls):
        ''' Set all "methods" as unexecuted.
            See: "method" in class description
        '''

        # Instead of change values from True to False, we choose safer method (delete and create object one more time).
        cls.methodToBool = {}
        cls.CreateListOfMethodsNames()

    @classmethod
    def CreateListOfMethodsNames(cls):
        ''' Adds all "methods" to "methodToBool" attribute with all values set to False.
            See: "method" in class description
        '''
        allAttributes = dir(SetUpManager)
        for name in allAttributes:
            if name[:5] == "SetUp":
                if name != "SetUp":
                    cls.methodToBool[getattr(SetUpManager, name)] = False

    @classmethod
    def ExecuteAllMethods(cls):
        ''' Execute all "methods" added to this class.
            See: "method" in class description
        '''
        for key in cls.methodToBool.keys():
                if cls.methodToBool[key] == False:
                    key()
                    cls.methodToBool[key] = True

    @classmethod
    def ExecuteIfHasNotBeenYet(cls, method):
        ''' Execute method if has not been executed yet.

        :param method: method
        '''
        for key in cls.methodToBool.keys():
            if method == key:
                if cls.methodToBool[key] == False:
                    method()
                    cls.methodToBool[key] = True

    ###################################################################################################################
    # "methods" #######################################################################################################
    ###################################################################################################################

    '''data_cointaners'''
    @classmethod
    def SetUpRadarRecord(cls):
        RadarRecord.numberOfRangefinderRecords = SETTINGS.COMMON_FOR_MANY.NUMBER_OF_RANGEFINDERS

    '''car_base'''
    @classmethod
    def SetUpCarTransformCalculator(cls):
        CarTransformCalculator.deltaTime = SETTINGS.BASE_CAR.DElTA_TIME

        CarTransformCalculator.velocityValue = SETTINGS.BASE_CAR.VALUE_OF_VELOCITY
        CarTransformCalculator.sideAccelerationFactor = SETTINGS.BASE_CAR.SIDE_ACCELERATION_FACTOR
        CarTransformCalculator.longitudinalAccelerationFactor = SETTINGS.BASE_CAR.LONGITUDINAL_ACCELERATION_FACTOR
        CarTransformCalculator.voluntaryChangeOfSlipAngle = SETTINGS.BASE_CAR.VOLUNTARY_CHANGE_OF_SLIP_ANGLE
        CarTransformCalculator.changeOfSlipAngleDuringReturning = SETTINGS.BASE_CAR.CHANGE_OF_SLIP_ANGLE_DURING_RETURNING
        CarTransformCalculator.maximalSlipAngle = SETTINGS.BASE_CAR.MAXIMAL_SLIP_ANGLE

    @classmethod
    def SetUpBaseCar(cls):
        cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpImagesManager)
        cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpBarrier)
        cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpMap)

        BaseCar.original_rect = ImagesManager.GetImage("car").get_rect()

        BaseCar.map = Map()
        BaseCar.map.LoadFromFile(PathsManager.GetPath("map"))

        BaseCar.maximalRandomRotChange = SETTINGS.BASE_CAR.MAXIMAL_RANDOM_ROTATION_CHANGE
        BaseCar.velocityValue = SETTINGS.BASE_CAR.VALUE_OF_VELOCITY

    '''car_radar_equipped'''
    @classmethod
    def SetUpRangefinderTransformCalculator(cls):
        RangefinderTransformCalculator.CalculateRelativeRots(SETTINGS.RADAR_EQUIPPED_CAR.RANGE_OF_RADAR, SETTINGS.COMMON_FOR_MANY.NUMBER_OF_RANGEFINDERS)

    @classmethod
    def SetUpRadarTransformCalculator(cls):
        cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpBaseCar)

        RadarTransformCalculator.CalculateOriginalRelativePos(BaseCar.original_rect, SETTINGS.RADAR_EQUIPPED_CAR.RADAR_COEFFICIENT)

    @classmethod
    def SetUpRadar(cls):
        Radar.numberOfRangefinders = SETTINGS.COMMON_FOR_MANY.NUMBER_OF_RANGEFINDERS

    '''car_trainable'''
    #None


    '''displayer'''
    @classmethod
    def SetUpCarRelatedSpritesContainer(cls):
        CarRelatedSpritesContainer.numberOfSrangefinders = SETTINGS.COMMON_FOR_MANY.NUMBER_OF_RANGEFINDERS

    @classmethod
    def SetUpCamera(cls):
        cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpBaseCar)

        BaseCar.map.CalculateSize()
        Camera.mapSize = BaseCar.map.size

        Camera.windowSize = Vector(SETTINGS.DISPLAYER.WINDOW_WIDTH, SETTINGS.DISPLAYER.WINDOW_HEIGHT)
        Camera.Create()

    @classmethod
    def SetUpDisplayer(cls):
        pg.init()

        Displayer.windowSize = Vector(SETTINGS.DISPLAYER.WINDOW_WIDTH, SETTINGS.DISPLAYER.WINDOW_HEIGHT)
        Displayer.backgroundColor = SETTINGS.DISPLAYER.BACKGROUND_COLOR
        Displayer.meshColor = SETTINGS.DISPLAYER.MESH_COLOR
        Displayer.framesPerSecond = SETTINGS.DISPLAYER.FRAMES_PER_SECOND

        Displayer.captionColor = SETTINGS.DISPLAYER.CAPTION_COLOR
        Displayer.captionFontName = SETTINGS.DISPLAYER.CAPTION_FONT_NAME
        Displayer.captionFontSize = SETTINGS.DISPLAYER.CAPTION_FONT_SIZE


        Displayer.ConnectSpritesManager()


    '''general_tools'''
    @classmethod
    def SetUpPathsManager(cls):
        pathToThisFile = os.path.dirname(os.path.abspath(__file__))
        PathsManager.mainPath = pathToThisFile.replace("Modules\\Settings", "")

        PathsManager.AddFile("car", "Assets\\sprites\\car.png")
        PathsManager.AddFile("barrier", "Assets\\sprites\\square.png")

        PathsManager.AddFile("map", "Assets\\maps\\map1.txt")
        TrainableCar.lengthOfCompleteDrive = 1300

        PathsManager.AddDirectory("albums", "Scripts\\data\\albums\\")

    @classmethod
    def SetUpImagesManager(cls):
        ImagesManager.Initialize()
        ImagesManager.AddImage("barrier", PathsManager.GetPath("barrier"))
        ImagesManager.AddImage("car", PathsManager.GetPath("car"), scale=0.5)

    '''genetics'''
    @classmethod
    def SetUpPattern(cls):
        cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpBrain)

        architecture = [Brain.inputTransformator.inputArchitecturalFactor] + SETTINGS.NEURAL_NETWORKS.NN_ARCHITECTURE_DEEP_FACTORS + [Brain.outputTransformator.outputArchitecturalFactor]
        Pattern.CalculateLength(architecture)

        Pattern.wageMin = SETTINGS.NEURAL_NETWORKS.WAGE_MIN
        Pattern.wageMax = SETTINGS.NEURAL_NETWORKS.WAGE_MAX


    @classmethod
    def SetUpFitnessEvaluator(cls):
        cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpRadar)
        cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpRadarRecord)
        cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpRadarTransformCalculator)

        FitnessEvaluator.verbose = True
        FitnessEvaluator.car = TrainableCar()


    @classmethod
    def SetUpEvolutonaryAlgorithm(cls):
        cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpPattern)

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        EvolutonaryAlgorithm.lverbose = True

        # INDIVIDUALS
        EvolutonaryAlgorithm.geneRandomizingFunction = Pattern.RandomWage
        EvolutonaryAlgorithm.lengthOfIndividual = Pattern.length

        #LAWS
        EvolutonaryAlgorithm.probabilityOfCrossing = SETTINGS.GENETICS.CROSSING.PROBABILITY
        EvolutonaryAlgorithm.crossingMethod = SETTINGS.GENETICS.CROSSING.METHOD
        EvolutonaryAlgorithm.crossingParameters = {}

        EvolutonaryAlgorithm.probabilityOfMutation = SETTINGS.GENETICS.MUTATION.PROBABILITY
        EvolutonaryAlgorithm.mutationMethod = SETTINGS.GENETICS.MUTATION.METHOD
        EvolutonaryAlgorithm.mutationParameters = {}
        EvolutonaryAlgorithm.mutationParameters['mu'] = SETTINGS.GENETICS.MUTATION.GAUSSIAN.MEAN_OF_THE_DISTRIBUTION
        EvolutonaryAlgorithm.mutationParameters['sigma'] = SETTINGS.GENETICS.MUTATION.GAUSSIAN.STD_DEVIATION_OF_THE_DISTRIBUTION
        EvolutonaryAlgorithm.mutationParameters['indpb'] = SETTINGS.GENETICS.MUTATION.PROBABILITY_OF_ATTRIBUTE_MUTATION

        EvolutonaryAlgorithm.selectionMethod = SETTINGS.GENETICS.SELECTION.METHOD
        EvolutonaryAlgorithm.selectionParameters = {}
        EvolutonaryAlgorithm.selectionParameters['tournsize'] = SETTINGS.GENETICS.SELECTION.TOURNAMENT.SIZE

        #MAKRO
        EvolutonaryAlgorithm.paramMu = SETTINGS.GENETICS.SIZE_OF_POPULATION_AFTER_SELECTION
        EvolutonaryAlgorithm.paramLambda = SETTINGS.GENETICS.SIZE_OF_POPULATION_BEFORE_SELECTION
        EvolutonaryAlgorithm.numberOfGenerations = SETTINGS.GENETICS.NUMBER_OF_GENERATIONS

        #STATISTICS
        EvolutonaryAlgorithm.dictWithStatistics = {}
        EvolutonaryAlgorithm.dictWithStatistics['min'] = SETTINGS.GENETICS.STATISTICS.MIN
        EvolutonaryAlgorithm.dictWithStatistics['max'] = SETTINGS.GENETICS.STATISTICS.MAX
        EvolutonaryAlgorithm.dictWithStatistics['avg'] = SETTINGS.GENETICS.STATISTICS.AVERAGE


        #GENERAL
        EvolutonaryAlgorithm.Prepare()

    '''geometry'''
    @classmethod
    def SetUpProjectionCalculator(cls):
        cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpBaseCar)

        ProjectionCalculator.SetRects(BaseCar.map.listOfBarriers)


    '''map'''
    @classmethod
    def SetUpBarrier(cls):
        cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpPathsManager)

        Barrier.baseSize = Vector(pg.image.load(PathsManager.GetPath("barrier")).get_size())

    @classmethod
    def SetUpMap(cls):
        Map.ConvertPos = lambda pos: [int(20*pos[0]), -int(20*pos[1])]
        Map.ConvertRot = lambda rot: rot
        Map.ConvertScale = lambda scale: [abs(coord)/5 for coord in scale]

        Map.margin = SETTINGS.MAP.MARGIN

    '''neural_networks'''
    @classmethod
    def SetUpInputTransformator(cls):
        InputTransformator.inputArchitecturalFactor = SETTINGS.COMMON_FOR_MANY.NUMBER_OF_RANGEFINDERS



    @classmethod
    def SetUpBrain(cls):
        cls.ExecuteIfHasNotBeenYet(SetUpManager.SetUpInputTransformator)

        Brain.deepArchitecturalFactors = SETTINGS.NEURAL_NETWORKS.NN_ARCHITECTURE_DEEP_FACTORS
        Brain.Create(InputTransformator, OutputTransformator)

    '''sprites'''
    @classmethod
    def SetUpSSmallSquare(cls):
        SSmallSquare.size = SETTINGS.SPRITES.SMALL_SQUARE_SIZE

        SRangefinder.color = SETTINGS.SPRITES.COLORS.RANGEFINDER_COLOR
        SRadar.color = SETTINGS.SPRITES.COLORS.RADAR_COLOR


    @classmethod
    def SetUpSRotatableRect(cls):
        SBarrier.baseImage = ImagesManager.GetImage("barrier")
        SCar.baseImage = ImagesManager.GetImage("car")




# In case we don't use "SetUp" method in some script.
SetUpManager.Reset()
