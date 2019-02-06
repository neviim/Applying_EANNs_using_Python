''' GEOMETRY
Author: Pawel Brysch
Date: Jan 2019

Geometry library which extend Pygame library. Main features which was added:
1. rotatable rects.
    In pygame colliders are rectangles with sides parallel to coordinate system axis. Now colliders can be rotated.
2. intersection between ray and other objects.
    There was no similar method in Pygame.

...
Classes
----------
Instantiable:
    Vector
    Point
    LinearEntity
        base class for Ray and Segment
    Ray
    Segment
    RotatedRect
Algorithms:
    ProjectionCalculator
        can calculate between ray and other objects.
'''

import pygame as pg
import numpy as np
from pygame import Rect
from enum import Enum, auto
import math
import copy




class Vector(pg.Vector2):
    ''' Extended Pygame.Vector
    '''
    def __init__(self, *args, **kwargs):
        super(Vector, self).__init__(*args, **kwargs)

    ''' Mathematical operations
    '''
    def __add__(self, other):
        return Vector((self.x + other[0], self.y + other[1]))

    def __sub__(self, other):
        return Vector((self.x - other[0], self.y - other[1]))

    def __rsub__(self, other):
        return Vector((other[0]-self.x, other[1]-self.y))

    def __rmul__(self, other):
        return Vector(other*self.x, other*self.y)

    ''' Iterating through coordinates (x and y)
    '''
    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < 2:
            if self.index == 0:
                result = self.x
            else:
                result = self.y
            self.index += 1
            return result
        else:
            raise StopIteration

    def Index(self, list0):
        ''' Method which returns index of Vector which is on the list.
            IMPORTANT: We assume that vector is on given list.
        '''
        index = 0
        while (list0[index] is None or list0[index] != self):
            index += 1
        return index

    def asInt(self):
        ''' Convert vector to tuple of ints. Sometimes Pygame requires that form of passing vector into its methods.
        '''
        return [int(self.x), int(self.y)]

    def rotate(self, p_float):
        '''
        :param p_float: angle
            Angle about which we want to rotate the vector (in degrees)
        :return: Vector
            Rotated vector
        '''
        return Vector(super(Vector, self).rotate(p_float))

    def ScaledByVector(self, vector):
        ''' Some Vector objects may be scaled in two dimensions. Size of object is an example. In that case we use this
            method.

        :param vector: Vector
        :return: Vector
            scaled vector
        '''
        return Vector(self.x*vector.x, self.y*vector.y)

    @property
    def angle(self):
        return None

    @angle.getter
    def angle(self):
        ''' Angle between vector and x-axis.
        '''
        return 360 - int(self.as_polar()[1])

    def Distance(self, point):
        ''' Distance between vector's end and point.
        '''
        return int(math.sqrt(self.SquaredDistance(point)))

    def SquaredDistance(self, point):
        ''' Squared distance between vector's end and point. Can improve performance of some algorithm (when extraction of a
            root is not necessary).
        '''
        return (self.x-point.x)**2 + (self.y-point.y)**2



class Point(Vector):
    pass



class LinearEntity:
    ''' Base class for Ray and Segment. Can be also considered as a line.

    ...
    Attributes
    ----------
    point1: Point
        some point on line.
    point2: Point
        some point on line. Different than point1.
    '''
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def IntersectionBetweenLinesContainting(self, entity):
        ''' We have two linear entities in this method. One is object that call this method. Second is "entity"
        argument. Both of them don't have to be lines. They can also be rays, etc. However, there always exist lines
        which contains those entities. This method finds intersection between them.

        :return: Point
            If intersection doesn't exist method will return None.
        '''

        # Let's assume (x1,y1), (x2,y2) are points of the linear entity. Hence, we can express a and b from linear
        # equation y=ax+b with the help of x1,y1,x2 and y2.
        # We can do it for both entities. Hence we have system of equations y=a1*x+b1, y=a2*x+b2.
        # We can transform those equation to general form of A1*x+A2*y=B. Hence set can be expressed in matrix-way as
        # A*(x,y)=B. Finally a is A matrix and b is B matrix. (a and b from code at this time).
        a = np.array([[self.point1.y - self.point2.y, self.point2.x - self.point1.x],
                      [entity.point1.y - entity.point2.y, entity.point2.x - entity.point1.x]])
        b = np.array([self.point2.x * self.point1.y - self.point1.x * self.point2.y,
                      entity.point2.x * entity.point1.y - entity.point1.x * entity.point2.y])
        try:
            # Use algorithm to solve linear equation
            result = np.linalg.solve(a, b)
            result = [int(coord) for coord in result]
            result = Point(result)
        except np.linalg.linalg.LinAlgError:
            result = None

        return result


class Ray(LinearEntity):
    ''' Ray, which we knows from geometry

    ...
    Attributes
    ----------
    baseVector: Vector
        vector that gives information about in which quarter vector is or to which axis vector is parallel. For example:
        [1,1] -> 1st quarter, [-1,-1] -> 3rd quarter, [1,0] -> parallel to x-axis, [-1,0] -> parallel to x_axis.
    '''
    def __init__(self, begin, pointOnRay=None, rot=None):
        ''' You can create ray in two different ways. Firstly you can pass any point on ray. Secondly you can pass
        rotation (it's assumed that x-axis has rotation=0).
        '''

        # Create point on ray if rotation was passed.
        if pointOnRay is None:
            pointOnRay = Vector(100, 0).rotate(-rot) + begin

        super(Ray, self).__init__(begin, pointOnRay)
        self.baseVector = None

        # For algorithms in future.
        self.CalculateBaseVector()

    def CalculateBaseVector(self):
        ''' Calculate base vector (see class description).
        '''
        self.baseVector = self.point2 - self.point1
        self.baseVector = Vector([np.sign(coord) for coord in self.baseVector])

    def BelongsCollinearPoint(self, point):
        ''' Check whether or nor point belongs to ray.
        Notice: point has to be collinear with ray.
        Algorithm presented below has improved performance, so it could be difficult to understand it.

        :param point: Point
        :return: bool
        '''
        result = False

        if self.baseVector.x != 0:
            if self.baseVector.x * (point.x - self.point1.x) >= 0:
                result = True
        else:
            if self.baseVector.y * (point.y - self.point1.y) >= 0:
                result = True

        return result

    def IntersectionWithSegment(self, segment):
        ''' Calculate intersection between object (which is a ray) and segment.

        :param segment: Segment
        :return: Point
            returns None if intersection don't exist
        '''
        result = None

        # Calculate intersection between directions of, consequently, ray and segment.
        potentialIntersection = self.IntersectionBetweenLinesContainting(segment)

        # Check if calculated point belongs both to ray and segment.
        if potentialIntersection is not None:
            if self.BelongsCollinearPoint(potentialIntersection) and segment.BelongsCollinearPoint(potentialIntersection):
                result = potentialIntersection

        return result


    def BeginningProjectionOnRect(self, rect):
        ''' Calculate projection of the ray's beginning on a given rectangle.

        :param rect: RotatedRect
        :return: Point
        '''
        nearestPoint = None
        squaredDistancesToPoints = {}

        # Designate set of common points for object (ray) and circumference of given rectangle
        for side in rect.listOfSides:
            intersection = self.IntersectionBetweenLinesContainting(side)

            if intersection is not None:
                if side.BelongsCollinearPoint(intersection):
                    squaredDistance = intersection.SquaredDistance(self.point1)
                    squaredDistancesToPoints[squaredDistance] = intersection

        # Find point in designed set which is nearest to the beginning of the object.
        try:
            minimalSquareOfDistance = min(squaredDistancesToPoints.keys())
            nearestPoint = squaredDistancesToPoints[minimalSquareOfDistance]
        except ValueError:
            pass

        return nearestPoint

    def BeginningProjectionOnSetOfRects(self, rects=None, setNewRects=False):
        ''' Calculate projection of the ray's beginning on given set of rectangles
            We use "ProjectionCalculator" class to achieve this goal.

        :param rects: list
            set of rectangles.
        :param setNewRects: bool
            pass True if "ProjectionCalculater" haven't received data about rectangles yet.
        :return: Point
        '''

        # Set new set of rectangles (optional)
        if setNewRects == True:
            ProjectionCalculator.SetRects(rects)

        # Calculate projection using "ProjectionCalculator"
        return ProjectionCalculator.ProjectionOfBeginningOfRay(self)




class Segment(LinearEntity):
    ''' Segment, which we knows from geometry

    ...
    Attributes
    ----------
    min_x, max_x, min_y, max_y: float
        extrema, e.q. min_x is minimal value of x-coordinate among point of segment. Useful for algorithms.
    type: TypeOfSegment
        see: "TypeOfSegment" implementation. Useful for algorithms.

    '''
    class TypeOfSegment(Enum):
        NORMAL = auto()
        PARALLEL_TO_X = auto()
        PARALLEL_TO_Y = auto()

    def __init__(self, point1, point2):
        super(Segment, self).__init__(point1, point2)

        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None

        self.type = None

        # Calculate attributes which will be useful in further applications.
        self.CalculateExtrema()
        self.CalculateType()

    def CalculateExtrema(self):
        ''' Calculate extrema (see: class description)
        '''

        self.min_x = min([point.x for point in [self.point1, self.point2]])
        self.max_x = max([point.x for point in [self.point1, self.point2]])
        self.min_y = min([point.y for point in [self.point1, self.point2]])
        self.max_y = max([point.y for point in [self.point1, self.point2]])

    def CalculateType(self):
        ''' Calculate type of object (see: class description)
        '''

        if self.min_x == self.max_x:
            self.type = self.TypeOfSegment.PARALLEL_TO_Y
        elif self.min_y == self.max_y:
            self.type = self.TypeOfSegment.PARALLEL_TO_X
        else:
            self.type = self.TypeOfSegment.NORMAL

    def BelongsCollinearPoint(self, point):
        ''' Check whether or nor point belongs to segment.
        Notice: point has to be collinear with segment.

        :param point: Point
        :return: bool
        '''

        result = False

        if self.type == Segment.TypeOfSegment.NORMAL:
            if self.min_x <= point.x <= self.max_x and self.min_y <= point.y <= self.max_y:
                result = True
        elif self.type == Segment.TypeOfSegment.PARALLEL_TO_X:
            if self.min_x <= point.x <= self.max_x:
                result = True
        elif self.type == Segment.TypeOfSegment.PARALLEL_TO_Y:
            if self.min_y <= point.y <= self.max_y:
                result = True

        return result


class RotatedRect:
    ''' Rectangle with the possibility of rotating.

    ...
    Attributes
    ----------
    pos: Point
        position
    rot: float
        rotation
    listOfCorners: list
    listOfSides: list
    listOfDiagonals: list
    original_rect: Pygame.Rect
        rectangle before rotation.
    limitingRect: Pygame.Rect
        non-rotated rectangle in which our object is inscribed. Useful for algorithms.
    '''

    def __init__(self):
        self.pos = None
        self.rot = None
        self.listOfCorners = [None] * 4
        self.listOfSides = []
        self.listOfDiagonals = []
        self.original_rect = None
        self.limitingRect = None


    def CreateCorners(self):
        ''' Decorator
        '''
        self.CalculateCorners()

    def CalculateCorners(self):
        ''' Each rectangle has four corners.
        '''

        # Calculate corners
        self.listOfCorners[0] = (Vector(self.original_rect.topleft) - self.original_rect.center).rotate(-self.rot) + self.pos
        self.listOfCorners[1] = (Vector(self.original_rect.topright) - self.original_rect.center).rotate(-self.rot) + self.pos
        self.listOfCorners[2] = (Vector(self.original_rect.bottomright) - self.original_rect.center).rotate(-self.rot) + self.pos
        self.listOfCorners[3] = (Vector(self.original_rect.bottomleft) - self.original_rect.center).rotate(-self.rot) + self.pos

        # Calculate limiting rectangle. See: "limitingRect" in class description.
        self.CalculateLimitingRect()

    def CalculateLimitingRect(self):
        ''' To understand what is "limitingRect" check class description.
        '''

        # Calculate extremas
        x_max = max([corner.x for corner in self.listOfCorners])
        x_min = min([corner.x for corner in self.listOfCorners])
        y_max = max([corner.y for corner in self.listOfCorners])
        y_min = min([corner.y for corner in self.listOfCorners])

        # Create limiting rectangle by definition
        self.limitingRect = Rect((x_min, y_min), (x_max - x_min, y_max - y_min))

    def CalculateSegments(self):
        ''' Calculate object's sides and diagonals.
        '''
        self.listOfSides = []
        self.listOfDiagonals = []

        # Create sides
        for i in range(4):
            self.listOfSides.append(Segment(self.listOfCorners[i - 1], self.listOfCorners[i]))

        # Create diagonals
        self.listOfDiagonals.append(Segment(self.listOfCorners[0], self.listOfCorners[2]))
        self.listOfDiagonals.append(Segment(self.listOfCorners[1], self.listOfCorners[3]))


    def CollideWithSetOfRRects(self, listOfRRects):
        ''' Check whether or not object collide with set of rectangles

        :param listOfRRects: list
            rectangles must be "RotatedRect" objects
        :return: bool
        '''

        result = False

        for rrect in listOfRRects:
            # Check if limiting rectangles of individual objects collide with each other. This condition improves
            # performance of all algorithm, because limiting rectangles are simpler object (Pygame.Rect), so it takes
            # less time to check whether they are collided or not.
            if self.limitingRect.colliderect(rrect.limitingRect):
                for posOfCorner in self.listOfCorners:
                    # Check if corner belongs to rect. Notice we are checking it in reference system associated with
                    # original rectangle (!) of checked rectangle, not with the rectangle itself.
                    if rrect.original_rect.collidepoint((posOfCorner - rrect.pos).rotate(rrect.rot) + rrect.original_rect.center) == True:
                        result = True
        return result


class FixedRotatedRect(RotatedRect):
    ''' Rectangle that will not be moved.
    '''
    pass

class MobileRotatedRect(RotatedRect):
    ''' Rectangle that will be moved.
    '''

    def UpdateCorners(self):
        ''' Decorator
        '''
        self.CalculateCorners()


class ProjectionCalculator:
    ''' Algorithm that can calculate projection of ray's beginning on set of rectangles (objects of "RotatedRectangle"
    class). Algorithm is not automatic. You have to use it's methods in the following order.

    1. Use "SetRects()" method.
    2. Use "ProjectionOfBeginningOfRay" method

    This architecture results from the fact that typically rectangles will be constant, so its not recommended to load
    them multiple times.

    ...
    Attributes
    ----------
    currentRay: Ray
        chosen ray. Algorithm will find his beginning's projection on set of rectangles
    rectsToCommonPoints: dict
        helper attribute. Connect rectangles from the chosen set with points that are common for them and chosen ray.
        If such points don't exist, value will be None. If such points are more than one (typical situation), algorithm
        will choose one of them as a value.
    nearestRect: RotatedRect
        helper attribute. It is rectangle which is on the chosen ray and is closest to the beginning of the ray.
    nearestPoint:
        helper attribute. It is point from "nearestRect" which is closest to the beginning of the ray.
    '''

    currentRay = None
    rectsToCommonPoints = {}

    nearestRect = None
    nearestPoint = None

    @classmethod
    def SetRects(cls, listOfRects):
        ''' Set set of rectangles which will be considered in this algorithm.
            See: "rectsToCommonPoints" description in class description.
        '''
        cls.rectsToCommonPoints = dict((barrier, None) for barrier in listOfRects)



    @classmethod
    def ProjectionOfBeginningOfRay(cls, ray):
        ''' Calculate projection of ray's beginning on set of rectangles.

        :param ray: Ray
        :return: Point
             projection of ray's beginning on set of rectangles. None if such projection doesn't exist.
        '''
        cls.currentRay = ray

        # Find points that are common for ray and for rectangles from the set.
        cls.FindCommonPoints()

        # Find rectangle which is closest to the beginning of the ray. Algorithm search only through rectangles with
        # common point
        cls.FindNearestRect()

        # Find nearest point if nearest rectangle exist.
        if cls.nearestRect is not None:
            cls.nearestPoint = cls.currentRay.BeginningProjectionOnRect(cls.nearestRect)
            return copy.deepcopy(cls.nearestPoint)
        else:
            return None

    @classmethod
    def FindCommonPoints(cls):
        ''' Find points that are common for ray and for rectangles from the set.
        '''
        for key in cls.rectsToCommonPoints.keys():
            cls.rectsToCommonPoints[key] = cls.CommonPointForCurrentRayAndRect(key)


    @classmethod
    def CommonPointForCurrentRayAndRect(cls, rect):
        ''' Find one common point for rectangle and ray.
            The idea of this method is that common point MUST be on one of the diagonals.

        :param rect: Rectangle
            rectangle chosen from the set (set which was passed at the start of the algorithm_.
        :return: Point
            Common point for rectangle and ray. If such points don't exist, value will be None.
            If such points is more than one (typical situation), algorithm will choose one of them as a value.
        '''

        # Check if ray intersects first diagonal.
        firstPotentialPoint = cls.currentRay.IntersectionWithSegment(rect.listOfDiagonals[0])
        if firstPotentialPoint is not None:
            return firstPotentialPoint
        else:
            # Check if ray intersects second diagonal.
            secondPotentialPoint = cls.currentRay.IntersectionWithSegment(rect.listOfDiagonals[1])
            if secondPotentialPoint is not None:
                return secondPotentialPoint
            else:
                return None

    @classmethod
    def FindNearestRect(cls):
        ''' Find rectangle which is closest to the ray's beginning. Algorithm search only through rectangles with common
            point.
            The idea of this method is that rect is nearest when his common point is closest to the beginning of the ray.
            Implementation is complicated, because:

            1. Some rectangles from dict "rectsToCommonPoints" has no common point. Hence "A" statement.
            2. We use squared distance instead of distance to improve performance.
        '''
        # Dictionary in which we will be searching rectangle with minimal squared distance from the beginning of the ray.
        squaredDistancesToRects = {}

        # Add items to dictionary
        for rect, point in cls.rectsToCommonPoints.items():
            # A - see: class description.
            if point is not None:
                # "point1" is the ray's beginning
                squaredDistance = point.SquaredDistance(cls.currentRay.point1)
                squaredDistancesToRects[squaredDistance] = rect

        # Find minimum in dictionary.
        try:
            minimalSquareOfDistance = min(squaredDistancesToRects.keys())
            cls.nearestRect = squaredDistancesToRects[minimalSquareOfDistance]
        except ValueError:
            pass

