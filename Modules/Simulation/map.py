''' MAP
Author: Pawel Brysch
Date: Jan 2019

Module contains classes which allow to create environment for drive simulations.

...
Classes
----------
Barrier:
    unit of environment
Map:
    the right environment. Can be considered as a set of barriers.
'''

from Modules.General.general_tools import FilesManager, BuiltInTypesConverter
from Modules.Simulation.geometry import FixedRotatedRect, Point, Vector
from pygame import Rect




class Barrier(FixedRotatedRect):
    ''' Unit of environment. Thanks to deriving from "FixedRotatedRect" object handle collisions.
        To create properly object of this class you have to perform 2 steps:
        1. Set "pos", "rot" and "scale" attributes
        2. Use "Create" method

    ...
    Attributes
    ----------
    baseSize: Vector
        class attribute. We assume that all barriers originated from one original barrier and their posterior shape is
        determined only by transformations (e.q. rotation, etc.) executed on that barrier.
    pos: Point
        position
    rot: float
        rotation
    scale: Vector
        scaling vector, e.q. [2,3] means you want to multiply width by 2 and height by 3
    '''
    baseSize = None

    def __init__(self):
        super(Barrier, self).__init__()
        self.pos = None
        self.rot = None
        self.scale = None

    def Create(self):
        ''' Use this method after setting attributes (see: class description).
        This method is necessary for the algorithms to work properly.
        '''
        self.CreateOriginalRect()
        self.CreateCorners()
        self.CalculateSegments()

    def CreateOriginalRect(self):
        ''' While "baseSize" is common for all barriers, each barrier has its "originalRect", which is shape of barrier
        after scaling BUT before rotating and translating.
        '''
        size = self.__class__.baseSize.ScaledByVector(self.scale)
        self.original_rect = Rect((0, 0), size)

class Map:
    ''' The right environment. Can be considered as a set of barriers.

    ...
    Attributes
    ----------
    ConvertPos: method
        class attribute. Gets tuple, return tuple.
    ConvertRot: method
        class attribute. Gets float, returns float
    ConvertScale: method
        class attribute. Gets tuple, returns tuple

    NOTE: the need to use the above methods results from fact, that typically maps are created in external environment
    (like Unity3D) with other coordinate systems.

    margin: int
        class attribute. Determine how wide (or how high) is lane between peripheral barriers and border of map.

    listOfBarriers: list

    carSuggestedPos: tuple
        suggested starting car's position on the map
    carSuggestedRot:
        suggested starting car's rotation on the map

    size: Vector
        border of map
    '''

    ConvertPos = None
    ConvertRot = None
    ConvertScale = None

    margin = None

    def __init__(self):
        self.listOfBarriers = []

        self.carSuggestedPos = None
        self.carSuggestedRot = None

        self.size = None

    def LoadFromFile(self, filename):
        ''' Load map from file.
            Example of proper constructed file:
            "   line_1:  100 200 270            // car: position (2 first), rotation (lat one)
                line_2:  300 400 90 2.5 0.5     // 1st barrier: position (2 first), rotation (middle), scale (2 last)
                line_3:  600 700 180 2 1        // 2nd barrier: position (2 first), rotation (middle), scale (2 last)
                line_4:  100 100 45 1.2 1.2     // 3rd barrier: position (2 first), rotation (middle), scale (2 last)
                .
                .
                .
                line_n+1:  350 100 30 1.5 1.5   // n'st barrier: position (2 first), rotation (middle), scale (2 last)
        '''

        lines = FilesManager.LinesFromFile(filename)

        # Divide the data into parts for the car and barriers respectively
        firstLine, rest = lines[0], lines[1:]

        # Convert to list of floats
        firstLine = BuiltInTypesConverter.StringToFloats(firstLine)

        # Unpack
        rawCarSuggestedPos, rawCarSuggestedRot = firstLine[0:2], firstLine[4]

        # Convert to our coordinate system.
        carSuggestedPos, carSuggestedRot = Map.ConvertPos(rawCarSuggestedPos), Map.ConvertRot(rawCarSuggestedRot)

        # Create  the right objects.
        self.carSuggestedPos, self.carSuggestedRot = Point(carSuggestedPos), carSuggestedRot

        # Steps in loop below are similar to steps above.
        for line in rest:
            line = BuiltInTypesConverter.StringToFloats(line)
            rawPos, rawRot, rawScale = line[0:2], line[4], line[2:4]
            pos, rot, scale = Map.ConvertPos(rawPos), Map.ConvertRot(rawRot), Map.ConvertScale(rawScale)

            barrier = Barrier()
            barrier.pos, barrier.rot, barrier.scale = Point(pos), rot, Vector(scale)

            # Calculate parameters necessary for algorithms.
            barrier.Create()

            self.listOfBarriers.append(barrier)

    def CalculateSize(self):
        ''' Calculate size of map. See: "size" and "margin" in class description.
        '''
        width = max([barrier.limitingRect.right for barrier in self.listOfBarriers])
        height = max([barrier.limitingRect.bottom for barrier in self.listOfBarriers])
        self.size = Vector(width + self.__class__.margin, height + self.__class__.margin)

