'''
TEST-II  ProjectionCalculator:IntersectionBetweenCurrentRayAndSegment(cls, segment):
'''
from Modules.Simulation.car_radar_equipped import Rangefinder
from Modules.Simulation.geometry import ProjectionCalculator
from addons.Tests.UnitTests.geometry_test.tools.geometry_test_tools import StaticTestDisplayer
from Modules.Simulation.geometry import Point, Segment, Ray
import unittest
import time

def func1(point):
    if point is not None:
        return [point.x, point.y]
    else:
        return None

rangefinder = Rangefinder()
rangefinder.pos = (100, 100)
rangefinder.rot = 90
ProjectionCalculator.currentRay = Ray(Point(rangefinder.pos), rot=rangefinder.rot)
ray = ProjectionCalculator.currentRay

segment = Segment(Point(50, 50), Point(150, 50))

start = time.time()
ray.IntersectionWithSegment(segment)
end = time.time()
print("Time of one calculation is equal: ", end - start)

class TestIfCurrentRayIntersectSegment(unittest.TestCase):

    def setUp(self):
        self.rangefinder = Rangefinder()

    def modAssertEqual(self, point1, point2):
        self.assertEqual(func1(point1), func1(point2))

    def test_normal(self):
        self.rangefinder.pos = (100, 100)
        self.rangefinder.rot = 315
        ProjectionCalculator.currentRay = Ray(Point(self.rangefinder.pos), rot=self.rangefinder.rot)
        ray = ProjectionCalculator.currentRay

        segment = Segment(Point(150, 0), Point(150, 200))

        self.modAssertEqual(ray.IntersectionWithSegment(segment), Point((150, 150)))
        segment = Segment(Point(50, 0), Point(50, 200))
        self.modAssertEqual(ray.IntersectionWithSegment(segment), None)
        segment = Segment(Point(150, 200), Point(150, 300))
        self.modAssertEqual(ray.IntersectionWithSegment(segment), None)

    def test_parallelToAxes(self):
        self.rangefinder.pos = (100, 100)
        self.rangefinder.rot = 0
        ProjectionCalculator.currentRay = Ray(Point(self.rangefinder.pos), rot=self.rangefinder.rot)
        ray = ProjectionCalculator.currentRay
        segment = Segment(Point(200, 50), Point(200, 150))

        self.modAssertEqual(ray.IntersectionWithSegment(segment), Point((200, 100)))


    def test_parallelToEachOther(self):
        self.rangefinder.pos = (100, 100)
        self.rangefinder.rot = 315
        ProjectionCalculator.currentRay = Ray(Point(self.rangefinder.pos), rot=self.rangefinder.rot)
        ray = ProjectionCalculator.currentRay

        segment = Segment(Point(200, 100), Point(300, 200))
        self.modAssertEqual(ray.IntersectionWithSegment(segment), None)


if __name__ == '__main__':
    unittest.main()

# testDisplayer = StaticTestDisplayer()
# testDisplayer.ifDrawSegments = True
# testDisplayer.ifDrawRays = True
#
# testDisplayer.AddRay(ProjectionCalculator.currentRay)
# testDisplayer.AddSegments([segment])
#
# testDisplayer.PlayAlbum()