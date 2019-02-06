'''
TEST LinearEntity::IntersectionBetweenLinesContainting(self, entity):
'''
from Modules.Settings.settings import *
import pygame as pg
# from pos_of_barrier_calculator import PosOfBarrierCalculator
from Modules.Simulation.geometry import LinearEntity, Point
import unittest
import time
from addons.Tests.UnitTests.geometry_test.tools.geometry_test_tools import printLine

def func1(point):
    if point is not None:
        return [point.x, point.y]
    else:
        return None

line1 = LinearEntity(Point(100, 100), Point(200, 100))
line2 = LinearEntity(Point(500, 300), Point(400, 300))

class TestIfCurIntersectionBetweenLinesContainting(unittest.TestCase):

    def test_normal(self):
        line1 = LinearEntity(Point(100, 100), Point(200, 200))
        line2 = LinearEntity(Point(150, 0), Point(160, 200))
        self.assertEqual(func1(line1.IntersectionBetweenLinesContainting(line2)), [157, 157])


    def test_one_line_parallel_to_one_axis(self):
        line1 = LinearEntity(Point(100, 100), Point(200, 200))
        line2 = LinearEntity(Point(150, 0), Point(150, 200))
        self.assertEqual(func1(line1.IntersectionBetweenLinesContainting(line2)), [150, 150])

        line1 = LinearEntity(Point(100, 100), Point(200, 200))
        line2 = LinearEntity(Point(100, 200), Point(300, 200))
        self.assertEqual(func1(line1.IntersectionBetweenLinesContainting(line2)), [200, 200])

        line1 = LinearEntity(Point(100, 100), Point(100, 200))
        line2 = LinearEntity(Point(0, 100), Point(200, 200))
        self.assertEqual(func1(line1.IntersectionBetweenLinesContainting(line2)), [100, 150])

        line1 = LinearEntity(Point(100, 100), Point(200, 100))
        line2 = LinearEntity(Point(100, 200), Point(300, 0))
        self.assertEqual(func1(line1.IntersectionBetweenLinesContainting(line2)), [200, 100])

    def test_two_lines_parallel_to_different_axes(self):
        line1 = LinearEntity(Point(100, 100), Point(100, 200))
        line2 = LinearEntity(Point(400, 300), Point(500, 300))
        self.assertEqual(func1(line1.IntersectionBetweenLinesContainting(line2)), [100, 300])

    def test_parallel_to_each_other_normal(self):
        line1 = LinearEntity(Point(100, 100), Point(200, 200))
        line2 = LinearEntity(Point(400, 200), Point(500, 300))
        self.assertEqual(func1(line1.IntersectionBetweenLinesContainting(line2)), None)

    def test_parallel_to_each_and_one_of_axes(self):
        line1 = LinearEntity(Point(100, 100), Point(100, 200))
        line2 = LinearEntity(Point(500, 300), Point(500, 200))
        self.assertEqual(func1(line1.IntersectionBetweenLinesContainting(line2)), None)

        line1 = LinearEntity(Point(100, 100), Point(200, 100))
        line2 = LinearEntity(Point(500, 300), Point(400, 300))
        self.assertEqual(func1(line1.IntersectionBetweenLinesContainting(line2)), None)

if __name__ == '__main__':
    unittest.main()

######################
# LIGHTGREY = (100, 100, 100)
# DARKGREY = (40, 40, 40)
#
# screen = pg.display.set_mode((SETTINGS.CAMERA.WINDOW_WIDTH, SETTINGS.CAMERA.WINDOW_HEIGHT))
#
#
# #switch that!!!
# ifHaveToQuit = False
# while ifHaveToQuit == False:
#
#     screen.fill(DARKGREY)
#
#     for x in range(0, SETTINGS.CAMERA.WINDOW_WIDTH, 100):
#         pg.draw.line(screen, LIGHTGREY, (x, 0), (x, SETTINGS.CAMERA.WINDOW_HEIGHT))
#     for y in range(0, SETTINGS.CAMERA.WINDOW_HEIGHT, 100):
#         pg.draw.line(screen, LIGHTGREY, (0, y), (SETTINGS.CAMERA.WINDOW_WIDTH, y))
#
#     printLine(line1, RED, screen)
#     printLine(line2, YELLOW, screen)
#
#     pg.display.flip()
#
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             ifHaveToQuit = True
#             pg.quit()