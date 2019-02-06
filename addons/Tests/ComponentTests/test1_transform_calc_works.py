'''
TEST CarTransformCalculator:NewTransform(cls, car, nextMove):
'''
from Modules.Settings.settings import *
import pygame as pg
from Modules.GUI.sprites import SBarrier, SCar
from Modules.Simulation.car_base import BaseCar
from Modules.Simulation.map import Map
# from test_helpers import test_Camera
from Modules.GUI.displayer import Camera
Vec = pg.math.Vector2
from Modules.General.general_tools import PathsManager
from Modules.General.general_types import Move
from Modules.Settings.set_up_manager import SetUpManager

SetUpManager.SetUpPathsManager()
SetUpManager.SetUpImagesManager()
SetUpManager.SetUpSRotatableRect()
SetUpManager.SetUpCarTransformCalculator()
SetUpManager.SetUpBarrier()
SetUpManager.SetUpMap()
SetUpManager.SetUpBaseCar()
SetUpManager.SetUpCamera()

'''
+) klasa Vector(Point) w point.py jako zwykly typedef
+) powinien miec value, ktore przyslania length
'''

#CAMERA
# cam = test_Camera(2300, 1400)
cam = Camera

amap = Map()
amap.LoadFromFile(PathsManager.GetPath("map"))
BaseCar.map = amap
listOfSBarriers = []

for barrier in amap.listOfBarriers:
    sbarrier = SBarrier()
    sbarrier.Create(barrier)
    listOfSBarriers.append(sbarrier)

class test_SCar(SCar):
    def __init__(self):
        super(test_SCar, self).__init__()

    def Create(self, car):
        self.pos = car.pos
        self.rot = car.rot
        self.CreateImage(car.rot)


car = BaseCar()
car.PlaceOnTheMap()
sob = test_SCar()
sob.Create(car)


screen = pg.display.set_mode((SETTINGS.DISPLAYER.WINDOW_WIDTH, SETTINGS.DISPLAYER.WINDOW_HEIGHT))
all_sprites = pg.sprite.Group()

group = pg.sprite.Group()
group.add(sob)

for sbarrier in listOfSBarriers:
    group.add(sbarrier)

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
        car.nextMove = Move.LEFT
    elif keys[pg.K_RIGHT] or keys[pg.K_d]:
        car.nextMove = Move.RIGHT
    else:
        car.nextMove = Move.NONE

    dt = clock.tick(30) / 1000.0

    car.PerformStep()
    sob.Create(car)

    #REST - part 2
    cam.FocusOn(sob)
    for sprite in group:
        screen.blit(sprite.image, cam.relativePos(sprite))
    pg.display.flip()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            ifHaveToQuit = True
            pg.quit()