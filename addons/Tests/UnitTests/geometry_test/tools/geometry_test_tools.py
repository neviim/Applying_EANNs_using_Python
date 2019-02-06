import pygame as pg
from Modules.Settings.settings import *
from Modules.GUI.sprites import SRadar, SRangefinder
from Modules.GUI.sprites import SCar
# from rangefinder import Rangefinder
# from radar import Radar
from Modules.Simulation.car_radar_equipped import Rangefinder
from Modules.Simulation.car_radar_equipped import Radar
from Modules.Simulation.car_trainable import TrainableCar

RED = (255,0,0)

Vec = pg.math.Vector2

def printSegment(segment, screen):
    x1 = segment.point1.x
    y1 = segment.point1.y
    x2 = segment.point2.x
    y2 = segment.point2.y

    pg.draw.line(screen, (255, 255, 0), [x1, y1], [x2, y2], 3)

def printRay(ray, screen):
    x1 = ray.point1.x
    y1 = ray.point1.y
    x2 = ray.point2.x
    y2 = ray.point2.y

    x2 = 100*(x2-x1) + x1
    y2 = 100*(y2-y1) + y1

    pg.draw.line(screen, (255,0,0), [x1, y1], [x2, y2], 3)

def printLine(line, color, screen):
    x1 = line.point1.x
    y1 = line.point1.y
    x2 = line.point2.x
    y2 = line.point2.y

    x2 = 100*(x2-x1) + x1
    y2 = 100*(y2-y1) + y1

    x1 = 2*(x1-x2) + x2
    y1 = 2*(y1-y2) + y2

    pg.draw.line(screen, color, [x1, y1], [x2, y2], 3)


class StaticTestDisplayer:
    def __init__(self):
        self.screen = pg.display.set_mode((SETTINGS.DISPLAYER.WINDOW_WIDTH, SETTINGS.DISPLAYER.WINDOW_HEIGHT))
        self.group = pg.sprite.Group()

        self.listOfSegments = []
        self.ifDrawSegments = False

        self.listOfRays = []
        self.ifDrawRays = False

        self.listOfLines = []
        self.ifDrawLines = False

    def AddSegments(self, alist):
        for segment in  alist:
            self.listOfSegments.append(segment)

    def AddRay(self, ray):
        self.listOfRays.append(ray)

    def AddLine(self, line):
        self.listOfLines.append(line)

    def Play(self):
        ifHaveToQuit = False
        while ifHaveToQuit == False:

            self.screen.fill(SETTINGS.DISPLAYER.BACKGROUND_COLOR)

            for x in range(0, SETTINGS.DISPLAYER.WINDOW_WIDTH, 100):
                pg.draw.line(self.screen, SETTINGS.DISPLAYER.MESH_COLOR, (x, 0), (x, SETTINGS.DISPLAYER.WINDOW_HEIGHT))
            for y in range(0, SETTINGS.DISPLAYER.WINDOW_HEIGHT, 100):
                pg.draw.line(self.screen, SETTINGS.DISPLAYER.MESH_COLOR, (0, y), (SETTINGS.DISPLAYER.WINDOW_WIDTH, y))

            self.group.draw(self.screen)

            if self.ifDrawSegments == True:
                for segment in self.listOfSegments:
                    printSegment(segment, self.screen)

            if self.ifDrawRays == True:
                for ray in self.listOfRays:
                    printRay(ray, self.screen)

            if self.ifDrawLines == True:
                for line in self.listOfLines:
                    printLine(line, RED, self.screen)

            pg.display.flip()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    ifHaveToQuit = True
                    pg.quit()


class test_SCar(SCar):
    def __init__(self):
        super(test_SCar, self).__init__()

    def Create(self, car):
        # self.SetPos(car.pos)
        self.pos = car.pos
        self.rot = car.rot
        self.CreateImage(self.rot)

class test_SRadar(SRadar):
    def __init__(self):
        super(test_SRadar, self).__init__()

    def Create(self, radar):
        self.pos = radar.pos


class test_SRangefinder(SRangefinder):
    def __init__(self):
        super(test_SRangefinder, self).__init__()

    def Create(self, rangefinder):
        pos = Vec(100, 0).rotate(-rangefinder.rot) + rangefinder.pos
        self.pos = pos

class test_SPoint(SRangefinder):
    def __init__(self):
        super(test_SPoint, self).__init__()

    def Create(self, point):
        x = point.x
        y = point.y
        self.pos = [x,y]


class ConditionallyWorkingRangefinder(Rangefinder):
    def __init__(self, number = None):
        # super(ConditionallyWorkingRangefinder, self).__init__(number)
        super(ConditionallyWorkingRangefinder, self).__init__()

    def MeasureDistance(self):
        if self.number == 0:
            super(ConditionallyWorkingRangefinder, self).MeasureDistance()

class RadarWithOneWorkingRangefinder(Radar):
    def __init__(self):
        super(RadarWithOneWorkingRangefinder, self).__init__()
        self.listOfRangefinders = [ConditionallyWorkingRangefinder(number) for number in range(SETTINGS.COMMON_FOR_MANY.NUMBER_OF_RANGEFINDERS)]

class CarWithOneWorkingRangefinder(TrainableCar):
    def __init__(self):
        super(CarWithOneWorkingRangefinder, self).__init__()
        self.radar = RadarWithOneWorkingRangefinder()