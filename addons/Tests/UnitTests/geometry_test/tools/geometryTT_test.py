'''
TEST printSegment(segment, screen):
'''
# from settings import *
# import pygame as pg
# from pos_of_barrier_calculator import LinearEntity
# from pobc_test_tools import printSegment
# segment = LinearEntity((100, 100), (200, 200))
#
# ######################
# LIGHTGREY = (100, 100, 100)
# DARKGREY = (40, 40, 40)
#
# screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#
# ifHaveToQuit = False
# while ifHaveToQuit == False:
#
#     screen.fill(DARKGREY)
#
#     for x in range(0, WINDOW_WIDTH, 100):
#         pg.draw.line(screen, LIGHTGREY, (x, 0), (x, WINDOW_HEIGHT))
#     for y in range(0, WINDOW_HEIGHT, 100):
#         pg.draw.line(screen, LIGHTGREY, (0, y), (WINDOW_WIDTH, y))
#
#     printSegment(segment, screen)
#
#     pg.display.flip()
#
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             ifHaveToQuit = True
#             pg.quit()


'''
TEST printRay(ray, screen):
'''
# from settings import *
# import pygame as pg
# from pos_of_barrier_calculator import LinearEntity
# from pobc_test_tools import printRay
#
# ray = LinearEntity((100, 100), (200, 200))
#
# ######################
# LIGHTGREY = (100, 100, 100)
# DARKGREY = (40, 40, 40)
#
# screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#
# ifHaveToQuit = False
# while ifHaveToQuit == False:
#
#     screen.fill(DARKGREY)
#
#     for x in range(0, WINDOW_WIDTH, 100):
#         pg.draw.line(screen, LIGHTGREY, (x, 0), (x, WINDOW_HEIGHT))
#     for y in range(0, WINDOW_HEIGHT, 100):
#         pg.draw.line(screen, LIGHTGREY, (0, y), (WINDOW_WIDTH, y))
#
#     printRay(ray, screen)
#
#     pg.display.flip()
#
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             ifHaveToQuit = True
#             pg.quit()

'''
TEST printLine(line, screen):
'''
# from settings import *
# import pygame as pg
# from pos_of_barrier_calculator import LinearEntity
# from pobc_test_tools import printLine
#
# line = LinearEntity((100, 100), (200, 200))
#
# ######################
# LIGHTGREY = (100, 100, 100)
# DARKGREY = (40, 40, 40)
#
# screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
#
# ifHaveToQuit = False
# while ifHaveToQuit == False:
#
#     screen.fill(DARKGREY)
#
#     for x in range(0, WINDOW_WIDTH, 100):
#         pg.draw.line(screen, LIGHTGREY, (x, 0), (x, WINDOW_HEIGHT))
#     for y in range(0, WINDOW_HEIGHT, 100):
#         pg.draw.line(screen, LIGHTGREY, (0, y), (WINDOW_WIDTH, y))
#
#     printLine(line, (255,0,0), screen)
#
#     pg.display.flip()
#
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             ifHaveToQuit = True
#             pg.quit()


'''
TEST StaticTestDisplayer:PlayAlbum(self)
'''
# from pobc_test_tools import StaticTestDisplayer
#
# testDisplayer = StaticTestDisplayer()
# testDisplayer.PlayAlbum()


'''
TEST StaticTestDisplayer:AddSegments(self, alist):
'''
# from pobc_test_tools import StaticTestDisplayer
# from pos_of_barrier_calculator import LinearEntity
#
# segment1 = LinearEntity((100, 100), (200, 200))
# segment2 = LinearEntity((400, 100), (200, 200))
#
# testDisplayer = StaticTestDisplayer()
# testDisplayer.ifDrawSegments = True
#
# testDisplayer.AddSegments([segment1, segment2])
#
# testDisplayer.PlayAlbum()

'''
TEST StaticTestDisplayer:AddRay(self, ray):
'''
# from pobc_test_tools import StaticTestDisplayer
# from pos_of_barrier_calculator import LinearEntity
#
# ray = LinearEntity((100, 100), (200, 200))
#
# testDisplayer = StaticTestDisplayer()
# testDisplayer.ifDrawRays = True
#
# testDisplayer.AddRay(ray)
#
# testDisplayer.PlayAlbum()

'''
TEST StaticTestDisplayer:AddLine(self, ray):
'''
# from pobc_test_tools import StaticTestDisplayer
# from pos_of_barrier_calculator import LinearEntity
#
# line = LinearEntity((100, 100), (200, 200))
#
# testDisplayer = StaticTestDisplayer()
# testDisplayer.ifDrawLines = True
#
# testDisplayer.AddLine(line)
#
# testDisplayer.PlayAlbum()