''' SPRITES
Author: Pawel Brysch
Date: Jan 2019

Module contains classes which allow create sprites, which are used to show the course of the experiment.

class MoreIntuitiveSprite(pg.sprite.Sprite):
    base class for all other classes in that module
class SSmallSquare(MoreIntuitiveSprite):
    base class for SRangefinder and SRadar
class SRangefinder(SSmallSquare):
    sprites which represents rangefinders
class SRadar(SSmallSquare):
    sprites which represents radars
class SRotatableRect(MoreIntuitiveSprite):
    base class for SBarrier and Scar
class SBarrier(SRotatableRect):
    sprites which represents barriers
class SCar(SRotatableRect):
    sprites which represents cars
'''


from Modules.General.general_tools import ImagesManager
import pygame as pg


#virtual
class MoreIntuitiveSprite(pg.sprite.Sprite):
    ''' Pygame sprite with useful property (see below), which makes setting position easier.
    '''
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

    @property
    def pos(self):
        return self.rect.center

    @pos.setter
    def pos(self, value):
        self.rect.center = value

#virtual
class SSmallSquare(MoreIntuitiveSprite):
    ''' Simple square with no rotation.

        ...
    Attributes
    ----------
    color: Color
        color of square. Must be set before initializing.
    size: Vector
        size of square. Must be set before initializing.
    '''
    color = None
    size = None

    def __init__(self):
        super(SSmallSquare, self).__init__()
        self.image = pg.Surface(SSmallSquare.size)
        self.image.fill(self.__class__.color)
        self.rect = self.image.get_rect()


class SRangefinder(SSmallSquare):
    ''' Sprite which represents rangefinder. It is separate class from SRadar, because in this way we can set different
        color for each type of object.
    '''
    pass

class SRadar(SSmallSquare):
    ''' Sprite which represents radar. It is separate class from SRadar, because in this way we can set different color
        for each type of object.
    '''
    pass


#virtual
class SRotatableRect(MoreIntuitiveSprite):
    ''' Sprite with useful property (see below), which makes changing "rect" attribute easier.

    ...
    Attributes
    ----------
    baseImage: Pygame.Image
        we assume, that all objects have similar images which originate from common one. This attribute is that image.
        Must be set before initializing.
    '''
    baseImage = None

    def __init__(self):
        super(SRotatableRect, self).__init__()
        self.rot = None
        self.image = self.__class__.baseImage
        self.rect = self.image.get_rect()

    @property
    def rectSize(self):
        return None

    @rectSize.setter
    def rectSize(self, value):
        ''' Change size of "rect" parameter.
            The reason why this property was created is that changing size of "rect" attribute requires three lines of
            code. Now we can do it in one line.

        :param value: Pygame.Rect
        '''
        buff = self.rect.center
        self.rect = value
        self.rect.center = buff


class SBarrier(SRotatableRect):
    ''' Sprite which represents barrier.

    ...
    Attributes
    ----------

    image: Pygame.Image
        This is not new attribute, but pygame.sprite.Sprite.image.
    '''
    def __init__(self):
        super(SBarrier, self).__init__()

    def Create(self, barrier):
        ''' Make sprite represent chosen barrier.

        :param barrier: Barrier
        '''

        # Translate sprite to the right place.
        self.pos = barrier.pos

        # Make sprite has proper rotation and scale.
        self.CreateImage(barrier.rot, barrier.scale)

    def CreateImage(self, rot, scale):
        ''' Helper method. Used only in Create() method.
            The reason why this method was created is that setting sprite's image required additional line for change
            it's "rect" attribute parameters.

        :param rot: float
            rotation
        :param scale: Vector
        '''

        # Create object's image by transforming base image for the class.
        self.image = ImagesManager.transformedImage(self.__class__.baseImage, scale, rot)

        # Set size of "rect" attribute. Notice, that position of "rect" attribute has been set before.
        self.rectSize = self.image.get_rect()



class SCar(SRotatableRect):
    ''' Sprite which represents car.

    ...
    Attributes
    ----------

    image: Pygame.Image
        see: "SBarrier" class documentation
    '''
    def __init__(self):
        super(SCar, self).__init__()


    def Update(self, record):
        ''' Make sprite represent car from the record.

        :param record: CarRecord
        '''

        # Translate sprite to the right place.
        self.pos = record.pos

        # Make sprite has proper image.
        self.CreateImage(record.rot)


    def CreateImage(self, rot):
        ''' The reason why this method was created is described in "SBarrier.CreateImage()" description.
            In this method we don't use scaling, because we assume, that "baseImage" was scaled at the beginning.
            In other words, scale of image is same for all cars.
        '''

        # Create object's image by transforming base image for the class.
        self.image = ImagesManager.rotatedImage(self.__class__.baseImage, rot)

        # Set size of "rect" attribute. Notice, that position of "rect" attribute was set before.
        self.rectSize = self.image.get_rect()

