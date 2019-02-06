'''
3. Map.FormatBarriers
'''

from Modules.Simulation.car_trainable import TrainableCar
import pygame as pg
Vec = pg.math.Vector2
from Modules.Settings.set_up_manager import SetUpManager
from Modules.Settings.settings import SETTINGS

SetUpManager.SetUp()

DELTA_POS = 5
DELTA_ROT = 5

class SteerableCar(TrainableCar):
    def __init__(self):
        super(SteerableCar, self).__init__()
        self.direction = None

    def CalculateNextMove(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.nextMove = "LEFT"
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.nextMove = "RIGHT"
        else:
            self.nextMove = "NONE"

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.direction = "FORWARD"
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.direction = "BACK"
        else:
            self.direction = None

    def PerformStep(self):

        if self.direction is not None:
            if self.direction == "FORWARD":
                self.pos += Vec(DELTA_POS, 0).rotate(-self.rot)
            elif self.direction == "BACK":
                self.pos += Vec(-DELTA_POS, 0).rotate(-self.rot)

        if self.nextMove == "LEFT":
            self.rot += DELTA_ROT
        elif self.nextMove == "RIGHT":
            self.rot -= DELTA_ROT

        self.UseRadar()
        self.CalculateNextMove()

        self.MoveRadar()

'''
TEST 
'''
from Modules.Settings.settings import *
from Modules.GUI.sprites import SBarrier
from Modules.Simulation.map import Map
from Modules.GUI.displayer import Camera
from Modules.Simulation.car_radar_equipped import RangefinderTransformCalculator
from addons.Tests.UnitTests.geometry_test.tools.geometry_test_tools import test_SPoint
'''
NR 3
'''
# from pos_of_barrier_calculator import ProjectionCalculator,
from Modules.Simulation.geometry import ProjectionCalculator, Point
from addons.Tests.UnitTests.geometry_test.tools.geometry_test_tools import test_SCar, test_SRadar, test_SRangefinder
from Modules.General.general_tools import PathsManager



#CAMERA
# cam = Camera(2300, 1400)
cam = Camera



#BARRIERS
amap = Map()
# amap.LoadFromFile(PathsManager.mapPath)
amap.LoadFromFile(PathsManager.GetPath("map"))
TrainableCar.map = amap

listOfSBarriers = []
for barrier in amap.listOfBarriers:
    sbarrier = SBarrier()
    sbarrier.Create(barrier)
    listOfSBarriers.append(sbarrier)

#PREPARATION
RangefinderTransformCalculator.CalculateRelativeRots(SETTINGS.RADAR_EQUIPPED_CAR.RANGE_OF_RADAR, SETTINGS.COMMON_FOR_MANY.NUMBER_OF_RANGEFINDERS)

for barrier in amap.listOfBarriers:
    barrier.CreateOriginalRect()
    barrier.CreateCorners()

ProjectionCalculator.SetRects(amap.listOfBarriers)

#CAR
car = SteerableCar()
car.PlaceOnTheMap()
car.CreateCorners()

scar = test_SCar()
scar.Create(car)

#RADAR
sradar = test_SRadar()
sradar.Create(car.radar)

#RANGEFINDERS
listOfRrangefinder = [test_SRangefinder() for i in range(SETTINGS.COMMON_FOR_MANY.NUMBER_OF_RANGEFINDERS)]
for srangefinder, rangefinder in zip(listOfRrangefinder, car.radar.listOfRangefinders):
    srangefinder.Create(rangefinder)

#TARGETS
listOfTargets = []
for i in range(SETTINGS.COMMON_FOR_MANY.NUMBER_OF_RANGEFINDERS):
    listOfTargets.append(test_SPoint())


#GROUP
group = pg.sprite.Group()
group.add(scar)
group.add(sradar)
for srangefinder in listOfRrangefinder:
    group.add(srangefinder)
for sbarrier in listOfSBarriers:
    group.add(sbarrier)
for target in listOfTargets:
    group.add(target)


#REST - part 0
pointZero = Point((0,0))
screen = pg.display.set_mode((SETTINGS.DISPLAYER.WINDOW_WIDTH, SETTINGS.DISPLAYER.WINDOW_HEIGHT))
clock = pg.time.Clock()
ifHaveToQuit = False

counter = 0

while ifHaveToQuit == False:
    #REST - part 1
    screen.fill(SETTINGS.DISPLAYER.BACKGROUND_COLOR)

    for x in range(0, SETTINGS.DISPLAYER.WINDOW_WIDTH, 100):
        pg.draw.line(screen, SETTINGS.DISPLAYER.MESH_COLOR, (x, 0), (x, SETTINGS.DISPLAYER.WINDOW_HEIGHT))
    for y in range(0, SETTINGS.DISPLAYER.WINDOW_HEIGHT, 100):
        pg.draw.line(screen, SETTINGS.DISPLAYER.MESH_COLOR, (0, y), (SETTINGS.DISPLAYER.WINDOW_WIDTH, y))

    dt = clock.tick(30) / 1000.0

    #FUNCTIONdd
    car.PerformStep()

    '''
    HERE
    '''
    # print(counter, car.radar.listOfRangefinders[0].distance, car.radar.listOfRangefinders[1].distance, car.radar.listOfRangefinders[2].distance)
    print(counter, [rangefinder.distance for rangefinder in car.radar.listOfRangefinders])
    counter += 1


    #UPDATING
    for target, rangefinder in zip(listOfTargets, car.radar.listOfRangefinders):
        if rangefinder.posOfBarrier is not None:
            target.Create(rangefinder.posOfBarrier)
        else:
            target.Create(pointZero)
    scar.Create(car)
    sradar.Create(car.radar)
    for srangefinder, rangefinder in zip(listOfRrangefinder, car.radar.listOfRangefinders):
        srangefinder.Create(rangefinder)

    #REST - part 2
    cam.FocusOn(scar)
    for sprite in group:
        screen.blit(sprite.image, cam.relativePos(sprite))
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            ifHaveToQuit = True
            pg.quit()