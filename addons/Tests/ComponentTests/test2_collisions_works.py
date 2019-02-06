
'''
TEST CollisionCalculator():IfCollided(cls, car, listOfBarriers):
'''
from Modules.Settings.settings import SETTINGS
from Modules.Settings.settings import *
import pygame as pg
Vec = pg.math.Vector2
from Modules.GUI.sprites import SBarrier, SCar
from Modules.GUI.sprites import SSmallSquare
from Modules.Simulation.car_trainable import TrainableCar
from Modules.Simulation.map import Map
from Modules.GUI.displayer import Camera
from Modules.Simulation.car_radar_equipped import RangefinderTransformCalculator
from Modules.General.general_tools import PathsManager
from Modules.Settings.set_up_manager import SetUpManager


SetUpManager.SetUp()

DELTA_POS = 5
DELTA_ROT = 5

RangefinderTransformCalculator.CalculateRelativeRots(SETTINGS.RADAR_EQUIPPED_CAR.RANGE_OF_RADAR, SETTINGS.COMMON_FOR_MANY.NUMBER_OF_RANGEFINDERS)

cam = Camera

amap = Map()
amap.LoadFromFile(PathsManager.GetPath("map"))
TrainableCar.map = amap


# for barrier in amap.listOfBarriers:
#     print("rect", barrier.original_rect, "pos", barrier.pos)
#     barrier.CalculateCorners()



listOfSBarriers = []

for barrier in amap.listOfBarriers:
    sbarrier = SBarrier()
    sbarrier.Create(barrier)
    listOfSBarriers.append(sbarrier)

class test_Car(TrainableCar):
    def __init__(self):
        super(test_Car, self).__init__()
        self.ifGo = False

    def PerformStep(self):

        if self.ifGo == True:
            self.pos += Vec(DELTA_POS, 0).rotate(-self.rot)

        if self.nextMove == "LEFT":
            self.rot += DELTA_ROT
        elif self.nextMove == "RIGHT":
            self.rot -= DELTA_ROT

class test_SCar(SCar):
    def __init__(self):
        super(test_SCar, self).__init__()

    def Create(self, car):
        # self.SetPos(car.pos)
        self.pos = car.pos
        self.rot = car.rot
        self.CreateImage(car.rot)

class test_SCorner(SSmallSquare):
    color = SETTINGS.SPRITES.COLORS.RANGEFINDER_COLOR
    def __init__(self):
        # super(test_SCorner, self).__init__(YELLOW)
        super(test_SCorner, self).__init__()
        self.image = pg.Surface((6, 6))
        self.image.fill(SETTINGS.SPRITES.COLORS.RANGEFINDER_COLOR)
        self.rect = self.image.get_rect()

class scornersOfBarrierContainer:
    def __init__(self):
        self.listOfScorners = [test_SCorner() for i in range(4)]

    def updateSCorners(self, barrier):
        for scorner, posOfCorner in zip(self.listOfScorners, barrier.listOfCorners):
            scorner.pos = posOfCorner

listOfSOBContainers = []
for barrier in  amap.listOfBarriers:
    barrier.CreateOriginalRect()
    barrier.CreateCorners()
    sobContainer = scornersOfBarrierContainer()
    sobContainer.updateSCorners(barrier)
    listOfSOBContainers.append(sobContainer)



car = test_Car()
a=2
car.PlaceOnTheMap()


car.CreateCorners()

listOfSCorners = []
for corner in car.listOfCorners:
    scorner = test_SCorner()
    scorner.pos = corner
    listOfSCorners.append(scorner)

sob = test_SCar()
sob.Create(car)


screen = pg.display.set_mode((SETTINGS.DISPLAYER.WINDOW_WIDTH, SETTINGS.DISPLAYER.WINDOW_HEIGHT))

#GROUP
group = pg.sprite.Group()
group.add(sob)

for sbarrier in listOfSBarriers:
    group.add(sbarrier)

for scorner in listOfSCorners:
    group.add(scorner)

for sobContainer in listOfSOBContainers:
    for scorner in sobContainer.listOfScorners:
        group.add(scorner)


#LOOP
clock = pg.time.Clock()
ifHaveToQuit = False
while ifHaveToQuit == False:

    screen.fill(SETTINGS.DISPLAYER.BACKGROUND_COLOR)

    for x in range(0, SETTINGS.DISPLAYER.WINDOW_WIDTH, 100):
        pg.draw.line(screen, SETTINGS.DISPLAYER.MESH_COLOR, (x, 0), (x, SETTINGS.DISPLAYER.WINDOW_HEIGHT))
    for y in range(0, SETTINGS.DISPLAYER.WINDOW_HEIGHT, 100):
        pg.draw.line(screen, SETTINGS.DISPLAYER.MESH_COLOR, (0, y), (SETTINGS.DISPLAYER.WINDOW_WIDTH, y))


    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] or keys[pg.K_a]:
        car.nextMove = "LEFT"
    elif keys[pg.K_RIGHT] or keys[pg.K_d]:
        car.nextMove = "RIGHT"
    else:
        car.nextMove = "NONE"

    if keys[pg.K_UP] or keys[pg.K_w]:
        car.ifGo = True
    else:
        car.ifGo = False

    dt = clock.tick(30) / 1000.0

    car.UpdateCorners()
    for scorner, posOfCorner in zip(listOfSCorners, car.listOfCorners):
        scorner.pos = posOfCorner

    car.PerformStep()
    sob.Create(car)

    #HERE
    # if CollisionCalculator.IfCollided(car, amap.listOfBarriers) == True:
    #     print("collided")
    if car.CollideWithSetOfRRects(amap.listOfBarriers) == True:
        print("collided")

    #DRAW
    pg.draw.rect(screen, SETTINGS.SPRITES.COLORS.RANGEFINDER_COLOR, car.limitingRect, 1)

    for barrier in amap.listOfBarriers:
        pg.draw.rect(screen, SETTINGS.SPRITES.COLORS.RANGEFINDER_COLOR, barrier.limitingRect, 1)

    cam.FocusOn(sob)
    for sprite in group:
        screen.blit(sprite.image, cam.relativePos(sprite))

    # group.draw(screen)
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            ifHaveToQuit = True
            pg.quit()