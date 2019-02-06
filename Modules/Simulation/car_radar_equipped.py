''' BASE CAR
Author: Pawel Brysch
Date: Jan 2019

Thanks to this module we can create driving units in our simulation, which can collide with environment. Also we can
measure their distance from the environment.

...
Classes
----------
RangefinderTransformCalculator:
    Rangefinder moves during simulation according to car. It need a class, which calculate transform parameters related
    to this motion. This is such a class.

Rangefinder:
    Basic unit, which can measure distance between self and environment. Can be installed on a car via a radar.

RadarTransformCalculator:
    Radar moves during simulation according to car. It need a class, which calculate transform parameters related to
    this motion. This is such a class.

Radar:
    Contains fixed number of rangefinders and is a manager for them.

RadarEquippedCar(BaseCar):
    Augmented version of BaseCar objects, which can additionally measure its distance from the environment.
'''

from Modules.Simulation.data_containers import RangefinderRecord, RadarRecord
from Modules.Simulation.car_base import BaseCar
from Modules.Simulation.geometry import Point, Vector,  Ray
import numpy as np





class RangefinderTransformCalculator:

    ''' Non-instantiable class. Calculates transform parameters related to motion of rangefinder.

    ...
    Attributes
    ----------
    listOfRelativeRots:
        Radar contains many rangefinders. Any of them is directed in different direction. Relative rotation (relativeRot
        here) are these direction in case when longitudinal axis of car is parallel to x-axis in our environment's
        coordinate system.
    '''
    listOfRelativeRots = []


    @classmethod
    def CalculateRelativeRots(cls, lrange, numberOfRangefinders):
        ''' See: "listOfRelativeRots" in class description.
            Has to bo exeuted at the beginning of the class's work

        :param lrange: float
            range of radar. In other words angle from which radar see the environment.
        :param numberOfRangefinders: int
            how many rangefinders radar has
        '''
        cls.listOfRelativeRots = []
        for rot in np.linspace(-lrange/2, lrange/2, numberOfRangefinders):
            cls.listOfRelativeRots.append(rot)

    @classmethod
    def NewTransform(cls, radar, number):
        ''' Method which updates rangefinder's transform parameters.

        :param radar: Radar
            Rangefinder is set on radar, so we need radar's position to find rangefinder's position.
        :param number: int
            Each rangefinder has to have its number. Hence, we know its rotation relative to car now.
        '''

        newPos = radar.pos
        newRot = radar.rot + cls.listOfRelativeRots[number]

        return newPos, newRot




class Rangefinder:
    ''' Object of this class can measure distance between self an environment. Can be installed on a car via a radar.

    ...
    Attributes
    ----------
    pos: Point
        position
    rot: float
        rotation
    posOfBarrier: Point
        position of that point of environment which is closest to the car in direction designated by rangefinder
    distance: int
        distance between car and point described in paragraph above.
    record: RangefinderRecord
        data container, where object can save its status.
    number: int
        object's number in radar which contains this object.
    '''
    def __init__(self, number=None):
        self.pos = None
        self.rot = None
        self.posOfBarrier = None
        self.distance = None
        self.record = RangefinderRecord()
        self.number = number


    def Save(self):
        ''' Save current status on record.
        '''
        self.record.pos = self.pos
        self.record.rot = self.rot
        self.record.posOfBarrier = self.posOfBarrier

    def MeasureDistance(self):
        ''' Calculate how far is car from the environment in direction designated by rangefinder.
        '''
        # Create ray from car in direction designated by rangefinder
        ray = Ray(Point(self.pos), rot=self.rot)

        # "SetOfRects" (elements of environment) has to be set before following line. That "set" is common
        # for all rangefinders and all moments, so this way has better performance.
        self.posOfBarrier = ray.BeginningProjectionOnSetOfRects()

        # Calculate distance. Distance is None when there is no point on the ray.
        try:
            self.distance = self.pos.Distance(self.posOfBarrier)
        except AttributeError:
            self.distance = None




class RadarTransformCalculator:
    ''' Non-instantiable class. Calculates transform parameters related to motion of radar.

    ...
    Attributes
    ----------
    originalRelativePos: Point
        Radar position if car is placed on the beginning of coordinate system.
    '''
    originalRelativePos = None

    @classmethod
    def CalculateOriginalRelativePos(cls, originalRectOfCar, coeff):
        ''' Calculate "originalRelativePos" which will be useful for following work of the class.

        :param originalRectOfCar: pygame.Rect
        :param coeff: float 0<...<1
            Determine where radar is placed on the car.
            Examples: coeff=0 -> radar is on the rear edge of car
                      coeff=0.5 -> radar is in the middle of car
                      coeff=1 -> radar is on the front edge of car
        '''

        # Calculate position of radar if topleft(!) corner of car is placed on the beginning of coordinate system.
        originalPos = Vector(coeff * originalRectOfCar.width, 0.5 * originalRectOfCar.height)

        # Calculate position of radar if center(!) of car is placed on the beginning of coordinate system.
        cls.originalRelativePos = originalPos - originalRectOfCar.center

    @classmethod
    def NewTransform(cls, car):
        '''Method updates rangefinder's transform parameters which it will has after step
        :param car: Car
            we need that argument to get its transform parameters
        '''

        # To understand line below read definition of "originalRelativePos" and description in
        # "CalculateOriginalRelativePos" method
        newPos = cls.originalRelativePos.rotate(-car.rot) + car.pos

        return newPos, car.rot




class Radar:
    ''' Object of this class contains rangefinders and manage them.

    ...
    Attributes
    ----------
    numberOfRangefinders: int
        class attribute. Common for all radars. To be set in external module (e.q. settings)
    pos: Point
        position
    rot: float
        rotation
    record: RadarRecord
        data container, where object can save its status
    '''

    numberOfRangefinders = None

    def __init__(self):
        self.pos = None
        self.rot = None

        # Create rangefinders.
        self.listOfRangefinders = [Rangefinder(_) for _ in range(self.__class__.numberOfRangefinders)]

        # Attach rangefinders's records to radar's record.
        self.record = RadarRecord(self.listOfRangefinders)


    def Save(self):
        ''' Save current status on record.
        '''
        self.record.pos = self.pos
        self.record.rot = self.rot

        for rangefinder in self.listOfRangefinders:
            rangefinder.Save()

    def MoveRangefinders(self):
        ''' We use this method from here (not from rangefinder), because its need radar's attributes (remember that
        radar is superior to rangefinders).
        '''

        for rangefinder in self.listOfRangefinders:
            rangefinder.pos, rangefinder.rot = RangefinderTransformCalculator.NewTransform(self, rangefinder.number)

    def MeasureDistances(self):
        ''' Take measurement from each rangefinder
        '''

        for rangeFinder in self.listOfRangefinders:
            rangeFinder.MeasureDistance()




class RadarEquippedCar(BaseCar):
    '''A car, which can measure its distance from the environment.

    ...
    Attributes
    ----------
    radar: Radar
        Thanks to this, objects can measure distances.
    '''
    def __init__(self):
        super(RadarEquippedCar, self).__init__()
        self.radar = Radar()

    def PerformStep(self):
        super(RadarEquippedCar, self).PerformStep()

        # Radar also is a object, so we need to move it.
        self.MoveRadar()

    def PlaceOnTheMap(self):
        super(RadarEquippedCar, self).PlaceOnTheMap()

        # Radar also is a object, so we need to move it.
        self.MoveRadar()

    def MoveRadar(self):
        ''' Move all object which are installed on the car.
        '''

        #Move radar
        self.radar.pos, self.radar.rot = RadarTransformCalculator.NewTransform(self)

        #Move rangefinders
        self.radar.MoveRangefinders()

    def UseRadar(self):
        ''' Decorator
        '''
        self.radar.MeasureDistances()