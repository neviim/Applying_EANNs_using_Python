''' BASE CAR
Author: Pawel Brysch
Date: Jan 2019

Thanks to this module you can create driving units in your simulation, which can collide with environment. It benefits
from developed geometry library called "geometry", which allow finding collisions between rotated object in contrast to,
pygame which doesn't have this feature.


...
Classes
----------
CarTransformCalculator:
    class which is used by BaseCar class to calculate transform parameters as position, velocity, etc.

BaseCar:
    base unit in simulation.
'''

from Modules.Simulation.geometry import Vector, MobileRotatedRect
from Modules.General.general_types import Move
import random

class CarTransformCalculator:
    '''
    Non-instantiable class used to calculate transform parameters of the object which use that parameters in its motion.
    Here we have just special case. You can easily create your own version.

    ...
    Attributes
    ----------
    deltaTime: float
        determine how long last one step of vehicle (or frame if we think analogically to games). We don't
        wait this time, because it is a simulation. To be set in external module (e.q. settings).
    sideAccelerationFactor: float
        determine how strong is impact of turning the vehicle on driving direction. To be set in external module
        (e.q. settings).
    longitudinalAccelerationFactor: float
        our model has a cruise control. Factor above determine how fast this feedback works. To be set in external
        module (e.q. settings).
    voluntaryChangeOfSlipAngle: float
        determine how fast slip angle is changing in result of turning. To be set in external module (e.q. settings).
    changeOfSlipAngleDuringReturning = float
        determine how fast vehicle is going back to driving straight ahead after stop turning. To be set in external
        module (e.q. settings).
    maximalSlipAngle = float
        determine maximal turning radius (it depends also on velocity). To be set in external module (e.q. settings).
    '''
    deltaTime = None
    sideAccelerationFactor = None
    longitudinalAccelerationFactor = None
    voluntaryChangeOfSlipAngle = None
    changeOfSlipAngleDuringReturning = None
    maximalSlipAngle = None


    @classmethod
    def NewTransform(cls, car, nextMove):
        ''' Method updates vehicle's transform parameters.

        :param car: BaseCar
            necessary arguments are inside that argument
        :param nextMove: GeneralTypes.Move
            vehicle decision about next step
        :return: transform parameters after step
        '''

        # Cases when vehicle want to change intensity of turning (turning more or less). We need to check if it is not
        # turned to its limits.
        if nextMove == Move.LEFT and car.slipAngle > -cls.maximalSlipAngle:
            car.slipAngle -= cls.voluntaryChangeOfSlipAngle
        elif nextMove == Move.RIGHT and car.slipAngle < cls.maximalSlipAngle:
            car.slipAngle += cls.voluntaryChangeOfSlipAngle
        else:
            # If vehicle don't want to change the intensity of turning it will go back to driving straight ahead by default,
            if car.slipAngle > 0:
                car.slipAngle -= cls.changeOfSlipAngleDuringReturning
            elif car.slipAngle < 0:
                car.slipAngle += cls.changeOfSlipAngleDuringReturning

        # Define some abbreviations
        f_s = cls.sideAccelerationFactor
        f_l = cls.longitudinalAccelerationFactor
        v_0 = cls.velocityValue

        # Determine acceleration
        sideAcceleration = Vector(f_s * car.slipAngle, 0).rotate(-car.rot + 90)
        longitudinalAcceleration = Vector(f_l * (v_0 - car.velocity.length()), 0).rotate(-car.rot)
        resultantAcceleration = sideAcceleration + longitudinalAcceleration

        # Determine transform parameters (we determined acceleration before. It was necessary for this step)
        newVelocity = car.velocity + cls.deltaTime * resultantAcceleration
        newPos = car.pos + cls.deltaTime * car.velocity

        return newPos, newVelocity.angle, newVelocity


class BaseCar(MobileRotatedRect):
    '''Base unit in simulation. Objects only moves and don't have any accessory features. The role of this class is to
       be used as parent class to more sophisticated cars.


    ...
    Attributes
    ----------
    map: Map
        class attribute. Common for all cars.
    original_rect: MobileRotatedRect
        class attribute.  We assume that cars in simulations have the same construction. Hence,  we need use line
        "self.original_rect = BaseCar.original_rect" in "__init__(self)", because algorithms of the parent class
        require to store that value as a instance attribute.
    maximalRandomRotChange: float
        class attribute. When car is placed on the map, we change slightly his rotation. This is maximum value of this
        change. It helps in evolutionary mechanism. To be set in external module (e.q. settings).
    velocityValue: float
        value of initial velocity. Same for each car. To be set in external module (e.q. settings).

    pos: Point
        position
    rot: float
        rotation
    nextMove: GeneralTypes.Move
        next planned move
    ifCollided: bool
        whether is collided with environment
    slipAngle: float
        how much car is turning at the moment
    velocity: Vector
        do not mistake with "velocityValue"

    '''
    map = None
    original_rect = None
    maximalRandomRotChange = None
    velocityValue = None

    def __init__(self):
        super(BaseCar, self).__init__()

        # Each of cars has the same original_rect. See: class description.
        self.original_rect = BaseCar.original_rect

        self.pos = None
        self.rot = None


        self.transformCalculator = CarTransformCalculator()

        self.nextMove = None
        self.ifCollided = False

        self.velocity = None
        self.slipAngle = 0


    def InitialVelocity(self):
        ''' Calculate initial velocity.
            Must be used before first step, but after setting "rot" attribute.

        :return: Vector
            velocity
        '''
        return Vector(self.__class__.velocityValue, 0).rotate(-self.rot)


    def PerformStep(self):
        ''' Perform one step (in physical way).
        '''

        self.pos, self.rot, self.velocity = self.transformCalculator.NewTransform(self, self.nextMove)

        # Necessary for algorithms to work properly
        self.UpdateCorners()

    def PlaceOnTheMap(self):
        ''' Place object on a a map.
        Map has to be assigned before calling this method.
        '''

        # Place at the "START" of the chosen map. Notice that we change primary rotation slightly.
        self.pos = self.__class__.map.carSuggestedPos
        self.rot = self.__class__.map.carSuggestedRot + random.randint(-self.__class__.maximalRandomRotChange, self.__class__.maximalRandomRotChange)

        # Necessary for algorithms to work properly
        self.CreateCorners()

        # Initialize rest of transform parameters.
        self.velocity = self.InitialVelocity()
        self.slipAngle = 0


    def CheckCollisions(self):
        ''' Check if car is collided with any element of the environment.
        '''
        self.ifCollided = self.CollideWithSetOfRRects(self.__class__.map.listOfBarriers)