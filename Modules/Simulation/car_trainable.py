''' TRAINABLE CAR
Author: Pawel Brysch
Date: Jan 2019

Module contains single class. See its description.
'''

from Modules.AI.NeuralNetworks.neural_networks import Brain
from Modules.Simulation.data_containers import BlackBox, CarRecord
from Modules.Simulation.car_radar_equipped import RadarEquippedCar
import copy




class TrainableCar(RadarEquippedCar):
    '''A car with built-in neural networks. It can use it to make decisions how to turn. Object contains also black box -
    - data container, which allow to record all drive.
    Object is a fully-equipped unit which can you use in your simulations.

    ...
    Attributes
    ----------
    lengthOfCompleteDrive: int
        class attribute. Same for each car. This attribute is equal to the step counter of the car, which is at the end
        of the race track.
        To be set in external module (e.q. settings). We recommend to set this attribute at this same place in code when
        we set map for experiments.


    brain: Brain
        neural networks which is used to decide about consecutive moves
    record: CarRecord
        data container, where object can save transform parameters, which describe one step
    blackBox: BlackBox
        data container, which allow to record all drive.
    stepCounter: int
        counter. Necessary to evaluate fitness during simulation.

    '''
    lengthOfCompleteDrive = None


    def __init__(self):
        super(TrainableCar, self).__init__()
        self.brain = Brain()
        self.record = CarRecord(self.radar.record)
        self.blackBox = BlackBox()
        self.stepCounter = 0


    def PerformStep(self):
        ''' Method which is looped during simulation. It contains all necessary methods to drive autonomously.
        '''
        self.UseRadar()
        self.CalculateNextMove()
        super(TrainableCar, self).PerformStep()
        self.CheckCollisions()


    def PerformDrive(self):
        ''' Proper simulation of drive.
            Thanks to this process we have determined step counter (which will be working as fitness later) and
            black box, which contains all drive saved on.
        '''

        # Initializion necessary before complex loop
        self.PrepareToDrive()

        # One step per iteration
        while self.ifCollided == False:
            self.PerformStep()
            self.Save()
            self.stepCounter += 1

            # Check if car is on the end of race track.
            if self.stepCounter == self.__class__.lengthOfCompleteDrive:
                break


    def PrepareToDrive(self):
        ''' Decorator
        '''
        self.PlaceOnTheMap()
        self.ResetMemory()


    def ResetMemory(self):
        ''' This method is useful for version of simulation, when at one moment drives only one car. Another version is
        when cars drive simultaneously. Then you don't need this method.
        '''

        # Reset black box
        self.blackBox = BlackBox()

        # Reset other attributes
        self.ifCollided = False
        self.stepCounter = 0

    def Save(self):
        ''' Save current status on record.
        '''
        self.record.pos = self.pos
        self.record.rot = self.rot
        self.radar.Save()

        # We need copy, because "record" attribute is changing dynamically.
        self.blackBox.AddCarRecord(copy.deepcopy(self.record))

    def CalculateNextMove(self):
        ''' Method which choosing next move using brain. "Brain.CalculateMove()" could be potentially complex method, so
            we need to pass all car's attributes using "self".
        '''
        self.nextMove = self.brain.CalculateMove(self)
