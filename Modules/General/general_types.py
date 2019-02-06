''' GENERAL TYPES
Author: Pawel Brysch
Date: Jan 2019

Module contains classes, which are basic types.
Classes are not connected which each other.
'''
from enum import Enum, auto

class Move(Enum):
    ''' Contains decision which you can take asked in which direction you want to turn.
    '''
    LEFT = auto()
    RIGHT = auto()
    NONE = auto()

class Colors:
    ''' Contains colors
    '''
    LIGHTGREY = (100, 100, 100)
    DARKGREY = (40, 40, 40)
    GOLD = (139, 105, 20)
    YELLOW = (255, 255, 0)
    LIGHTBROWN = (238, 207, 161)