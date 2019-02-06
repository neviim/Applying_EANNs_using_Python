''' DISPLAYER
Author: Pawel Brysch
Date: Jan 2019

Module contains classes which allow display course of the experiment.

DEFINITIONS:
Track - saved drive of single generation of cars
Album - saved drive of all generations of cars (entire course of the experiment)
Frame - image on the displayer at the chosen moment. We usually display many frames per one second.

IMPORTANT:
Each generation has the same number of cars (this information should help to understand solutions applied in this
module).

...
Classes
----------
CarRelatedSpritesContainer:
    object contains spites related with one car
SpritesManager:
    contains all sprites which are displayed and update them
Camera:
    allow displayer to change point of view
Displayer:
    core unit with loop similar to game loop
'''


from Modules.GUI.sprites import SRadar, SRangefinder, SBarrier, SCar
import pygame as pg


class CarRelatedSpritesContainer:
    ''' Object contains spites related with one car and can update them.

    ...

    Attributes
    ----------

    self.scar: SCar
    self.sradar: SRadar
    self.listOfSrangefinders: list
        list of "SRangefinder" objects
    self.frameNumber: int
        which frame will be displayed next
    self.blackBox: BlackBox
        data container from which object load new transform parameters (position, etc.) before each frame.
    '''
    numberOfSrangefinders = None

    def __init__(self):
        self.scar = SCar()
        self.sradar = SRadar()
        self.listOfSrangefinders = [SRangefinder() for _ in range(self.__class__.numberOfSrangefinders)]

        self.frameNumber = None
        self.blackBox = None

    @property
    def sprites(self):
        return None

    @sprites.getter
    def sprites(self):
        ''' Thanks to this we have all sprites which object contains in one statement.
        '''
        return [self.scar, self.sradar] + self.listOfSrangefinders

    def SetNewBlackBox(self, blackBox):
        ''' Set new black box and reset frameNumber from previous track.
        Used at the beginning of displaying a new track.

        :param blackBox: BlackBox
        '''
        self.frameNumber = 0
        self.blackBox = blackBox

    def LoadFromNextRecord(self):
        ''' Update sprites. If there is no more data (car ended its race), nothing changes (sprites remain the same).
            Used one time per one frame.
        '''
        try:
            self.LoadFromRecord(self.blackBox.listOfCarRecords[self.frameNumber])
            self.frameNumber += 1
        except IndexError:
            pass

    def LoadFromRecord(self, record):
        ''' Helper method. Thanks to this sprites can change their transform parameters as it is stated in record.

        :param record: CarRecord
        '''

        # Update sprite of car
        self.scar.Update(record)

        # Update sprite of radar
        self.sradar.pos = record.radarRecord.pos

        # Update sprites of rangefinders.
        for srangefinder, rangefinderRecord in zip(self.listOfSrangefinders, record.radarRecord.listOfRangefinderRecords):
            srangefinder.pos = rangefinderRecord.posOfBarrier

class SpritesManager:
    ''' Contains all sprites which are displayed and update that sprites during displaying.

    ...

    Attributes
    ----------
    sprites: pygame.sprite.Group
        all contained sprites. Attribute shared with "displayer" class.
    listOfCRSContainers : list
        see: "CarRelatedSpritesContainer" class description
    bestCarContainer: CarRelatedSpritesContainer
        container which contains sprites related with car, which drive was longest (in current showed generation).
        Camera focuses on that car.
    '''

    sprites = None
    listOfCRSContainers = []
    bestCarContainer = None

    @classmethod
    def CreateSBarriers(cls, map):
        ''' Create barriers' sprites. Used at the beginning of play.

        :param map: Map
            contains barriers, which can be use as templates to create sprites (named "sbarriers" here)
        '''

        # Create barriers
        listOfSBarriers = [SBarrier() for _ in map.listOfBarriers]
        for sbarrier, barrier in zip(listOfSBarriers, map.listOfBarriers):
            sbarrier.Create(barrier)

        # Add them to set of all displayed sprites.
        cls.sprites.add(listOfSBarriers)

    @classmethod
    def CreateCarRelatedSprites(cls, numberOfBlackBoxes):
        ''' Create sprites related with cars. Used at the beginning of play.

        :param numberOfBlackBoxes: int
            how many black boxes (which is equal to how many cars) is in single generation
        '''

        # Create sprites related with cars. Notice than at the beginning sprites are empty (They will be filled before
        # first frame).
        cls.listOfCRSContainers = [CarRelatedSpritesContainer() for _ in range(numberOfBlackBoxes)]

        # Add them to set of all displayed sprites.
        for crsContainer in cls.listOfCRSContainers:
            cls.sprites.add(crsContainer.sprites)

    @classmethod
    def SetNewTrack(cls, track):
        ''' Used at the beginning of playing next track.

        :param track: Track
            next track to be played
        '''

        # Set new black boxes for containers
        for crsContainer, blackBox in zip(cls.listOfCRSContainers, track.listOfBlackBoxes):
            crsContainer.SetNewBlackBox(blackBox)

        # Find container related with best car. See: class description.
        # Remember that although container was initialized only at the beginning of play, their black boxes are changing.
        # So in every track another container has the longest black box. Each time we have to find it.
        cls.FindBestCarContainer()

    @classmethod
    def FindBestCarContainer(cls):
        ''' Find container which contains sprites related with car, which drive was the longest.
        '''

        # Create dictionary which connect containers with lengths of theirs black boxes.
        lengthsToContainers = dict((container, container.blackBox.numberOfCarRecords) for container in cls.listOfCRSContainers)

        # Get container with longest black box.
        cls.bestCarContainer = max(lengthsToContainers, key=lengthsToContainers.get)

    @classmethod
    def UpdateCarRelatedSprites(cls):
        ''' Update sprites related with all displayed cars. Used before each frame.
        '''

        for crsContainer in cls.listOfCRSContainers:
            crsContainer.LoadFromNextRecord()


class Camera:
    ''' Allow displayer to change point of view.

    IMPORTANT
    Camera viev is rectangle inside map. It is what you see and have same size as window.
    Let's define two reference systems. General system have beginning at the left top corner of the map. Relative system,
    otherwise, at the top left corner of camera view.

    ...

    Attributes
    ----------

    mapSize: Vector
        size of map. To be set in external module (e.q. settings).
    windowSize: Vector
        size of application window. To be set in external module (e.q. settings).

    restrictingRect: pygame.Rect
        rectangle in which left top corner of camera view can be. Notice that this rectangle is smaller than map,
        because we don't want to see things beyond the map.
    targetRelativePos: Vector
        position of target in relative system (see: class description). Ultimately constant (center of camera view).
    topleftCornerPos: Vector
        position of left top corner of camera view in general system.
    '''

    mapSize = None
    windowSize = None

    restrictingRect = None
    targetRelativePos = None
    topleftCornerPos = None

    @classmethod
    def Create(cls):
        ''' Create attributes needed for the camera to work. See their descriptions in class description.
            Method must be executed at the beginning of displayer work.
        '''
        cls.restrictingRect = pg.Rect(0, 0, cls.mapSize.x - cls.windowSize.x, cls.mapSize.y - cls.windowSize.y)
        cls.targetRelativePos = 0.5 * cls.windowSize

    @classmethod
    def FocusOn(cls, target):
        ''' Set the target for which camera will follow.
        '''

        # Ultimately target should be at the center of view.
        cls.topleftCornerPos = target.rect.center - cls.targetRelativePos

        # If we are close to the border we need to move view towards center of the map. For this purpose we are using
        # restricting rectangle.
        if cls.topleftCornerPos.x < cls.restrictingRect.left:
            cls.topleftCornerPos.x = cls.restrictingRect.left
        elif cls.topleftCornerPos.x > cls.restrictingRect.right:
            cls.topleftCornerPos.x = cls.restrictingRect.right

        if cls.topleftCornerPos.y < cls.restrictingRect.top:
            cls.topleftCornerPos.y = cls.restrictingRect.top
        elif cls.topleftCornerPos.y > cls.restrictingRect.bottom:
            cls.topleftCornerPos.y = cls.restrictingRect.bottom

    @classmethod
    def relativePos(cls, sprite):
        ''' Calculate position of target in relative system.
        It will be used by displayer to draw the view.
        '''
        return sprite.rect.topleft - cls.topleftCornerPos




class Displayer:
    ''' Core unit with loop similar to game loop

    ...

    Attributes
    ----------

    sprites: pygame.sprite.Group()
        Set of displayed sprites. Shared with "spritesManager" attribute.
    spritesManager: SpritesManager
        See: "SpritesManager" class documentation

    camera: Camera
        See: "Camera" class documentation

    clock: pygame.time.Clock()
        Breaks between frames should be the same. It helps us to achieve that by measure time.
    framesPerSecond: int
        how many frames will be displayed per second.


    screen: pygame.Surface
        core of the object. Can be considered as interior of the window, which will be displayed.
    windowSize: Vector
        Size of window. To be set in external module (e.q. settings).
    backgroundColor: Color
    meshColor: Color

    caption: pygame.Surface
        caption. In our displayer it will contains current displayed generations's number.
    captionFont: pygame.Font
        font of the caption

    captionColor: Color
        To be set in external module (e.q. settings).
    captionFontName: str
        To be set in external module (e.q. settings).
    captionFontSize: int
        To be set in external module (e.q. settings).

    map: Map
        We have two data structures which contains data about sprites: maps and albums. Albums are different for each
        experiment, while maps are typically common for many experiment. Since it will be considered as attribute.
    numberOfCars: int
        How many cars there is in a single generation in the experiment.
    '''

    sprites = pg.sprite.Group()
    spritesManager = SpritesManager

    camera = Camera

    clock = pg.time.Clock()
    framesPerSecond = None

    screen = None
    windowSize = None
    backgroundColor = None
    meshColor = None

    caption = None
    captionFont = None

    captionColor = None
    captionFontName = None
    captionFontSize = None

    album = None
    numberOfCars = None

    @classmethod
    def ConnectSpritesManager(cls):
        ''' Makes that both displayer and sprites's manager works on the same object.
            Must be executed before using "PlayAlbum" method.
        '''
        cls.spritesManager.sprites = cls.sprites

    @classmethod
    def PlayAlbum(cls, album):
        ''' Main method of this class. Use if you want to watch how the experiment went through.
        '''

        # Get number of cars in single generation. It will be used later to create appropriate number of sprites.
        cls.numberOfCars = album.listOfTracks[0].numberOfBlackBoxes

        # Create screen on which everything will be drawn
        cls.CreateScreen()

        # Create sprites which will be drawn on the screen.
        cls.CreateSprites()

        # Create caption. See: "caption" in class description.
        cls.CreateCaption()

        # Album are divided into tracks. Hence this loop.
        for track in album.listOfTracks:
            cls.PlayTrack(track)

    @classmethod
    def CreateScreen(cls):
        ''' Creates screen.
            See: "screen" in class description.
        '''
        cls.screen = pg.display.set_mode(cls.windowSize.asInt())

    @classmethod
    def CreateSprites(cls):
        ''' Creates sprites.
            From this moment number of sprites is constant. They will only change.
        '''
        cls.spritesManager.CreateSBarriers(cls.map)
        cls.spritesManager.CreateCarRelatedSprites(cls.numberOfCars)

    @classmethod
    def CreateCaption(cls):
        ''' Creates font of the caption
            See: "caption" in class description.
        '''
        cls.captionFont = pg.font.SysFont(cls.captionFontName, cls.captionFontSize)

    @classmethod
    def PlayTrack(cls, track):
        ''' Helper function.
            It's kind of game loop.

        :param track: Track
        '''

        # Manager will work on every iteration of loop, so at the beginning we have to pass him new data.
        cls.spritesManager.SetNewTrack(track)

        # Core loop. 1 iteration = 1 frame.
        for _ in range(track.length):
            cls.Wait()
            cls.UpdateSprites()
            cls.UpdateCaption(track)
            cls.DrawFrame()

    @classmethod
    def Wait(cls):
        ''' Freeze the work of the program.
        '''
        cls.dt = cls.clock.tick(cls.framesPerSecond) / 1000.0

    @classmethod
    def UpdateSprites(cls):
        ''' Perform necessary updates on sprites in order to display them properly in next frame.
        '''
        cls.spritesManager.UpdateCarRelatedSprites()

    @classmethod
    def UpdateCaption(cls, track):
        ''' Increment number of generation displayed on the screen.

        :param track: Track
            need to get its number in order to show it on screen.
        '''
        cls.caption = cls.captionFont.render("Generation no " + str(track.number + 1), True, cls.captionColor)

    @classmethod
    def DrawFrame(cls):
        ''' Draw frame.
            The process has two steps.
            1. Draw everything on "virtual screen".                        blit() method
            2. Update screen (make it be same as "virtual screen").        flip() method
        '''

        # Focus camera on chosen target.
        # It determines which sprites will be displayed on the screen
        cls.camera.FocusOn(cls.spritesManager.bestCarContainer.scar)

        # Draw background
        cls.DrawBackground()

        # Draw sprites
        for sprite in cls.sprites:
            cls.screen.blit(sprite.image, cls.camera.relativePos(sprite))

        # Draw caption
        cls.screen.blit(cls.caption, (cls.camera.windowSize.x - 210, 10))

        # Update screen.
        pg.display.flip()

    @classmethod
    def DrawBackground(cls):
        ''' Draw view background.
        '''

        # Set color of view's background.
        cls.screen.fill(cls.backgroundColor)

        # Draw mesh (vertical and horizontal lines).
        for x in range(0, cls.screen.get_width(), 100):
            pg.draw.line(cls.screen, cls.meshColor, (x, 0), (x, cls.screen.get_height()))
        for y in range(0, cls.screen.get_height(), 100):
            pg.draw.line(cls.screen, cls.meshColor, (0, y), (cls.screen.get_width(), y))


