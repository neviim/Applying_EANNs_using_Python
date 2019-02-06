'''
TEST: upgradeAttribute(attributeName, object, newClass):
'''
#
# from album import CarRecord, RadarRecord
# from TESTS.SPECIFIC_LOGIC.album.auxilary_classes import upgradeAttribute, comparable_RecordOfRadar
#
# roc = CarRecord()
# roc.recordOfRadar = RadarRecord()
# roc.recordOfRadar.pos = [1, 2]
# roc.recordOfRadar.rot = [3]
#
# upgradeAttribute("recordOfRadar", roc, comparable_RecordOfRadar)
#
# look_at_that = None

'''
TEST: upgradeAttribute(attributeName, object, newClass):
'''
# from album import RadarRecord
# from TESTS.SPECIFIC_LOGIC.album.auxilary_classes import upgradeElements, comparable_RecordOfRadar
# from point import Point
#
#
# listOfRorads = []
#
# for i in range(3):
#     rorad = RadarRecord()
#     rorad.pos = Point([7, 8])
#     rorad.rot = 9
#     for roran in  rorad.listOfRORs:
#         roran.pos = Point([1, 2])
#         roran.rot = 3
#
#     listOfRorads.append(rorad)
#
#
# upgradeElements(listOfRorads, comparable_RecordOfRadar)
#
# look_at_that = None



'''
TEST: comparable_RecordOfRangefinder:__eq__(self, other):
'''
# from TESTS.SPECIFIC_LOGIC.album.auxilary_classes import comparable_RecordOfRangefinder
# roc1 = comparable_RecordOfRangefinder()
# roc1.pos = [1, 2]
# roc1.rot = 3
# roc1.posOfBarrier = [4, 5]
# roc2 = comparable_RecordOfRangefinder()
# roc2.pos = [1, 2]
# roc2.rot = 3
# roc2.posOfBarrier = [4, 5]
#
# if roc1 == roc2:
#     print("rowne")

'''
TEST: AlbumPrinter
'''

'''
TEST: comparable_RecordOfCar:Create(self, other):
'''
# from TESTS.SPECIFIC_LOGIC.album.auxilary_classes import comparable_RecordOfCar
# from album import CarRecord
# from point import Point
#
# roc1 = CarRecord()
# roc1.pos = Point([10, 11])
# roc1.rot = 12
# roc1.recordOfRadar.pos = Point([7, 8])
# roc1.recordOfRadar.rot = 9
#
# for roran in  roc1.recordOfRadar.listOfRORs:
#     roran.pos = Point([10, 11])
#     roran.rot = 3
#
# roc2 = comparable_RecordOfCar()
# roc2.Create(roc1)
#
# look_at_that = None


'''
TEST: comparable_BlackBox::__eq__(self, other):
'''
# from TESTS.SPECIFIC_LOGIC.album.auxilary_classes import comparable_BlackBox
# from album import CarRecord
# from point import Point
# import copy
# import unittest
#
# class Testcomparable_BlackBox(unittest.TestCase):
#
#     def setUp(self):
#         roc1 = CarRecord()
#         roc1.pos = Point([10, 11])
#         roc1.rot = 12
#         roc1.recordOfRadar.pos = Point([7, 8])
#         roc1.recordOfRadar.rot = 9
#
#         for roran in roc1.recordOfRadar.listOfRORs:
#             roran.pos = Point([1, 2])
#             roran.rot = 3
#
#         roc2 = copy.deepcopy(roc1)
#         roc3 = copy.deepcopy(roc1)
#
#         self.blackbox1 = comparable_BlackBox()
#         self.blackbox1.AddCarRecord(roc1)
#         self.blackbox1.AddCarRecord(roc2)
#         self.blackbox1.AddCarRecord(roc3)
#
#         self.blackbox2 = copy.deepcopy(self.blackbox1)
#
#     def test_equal(self):
#         self.assertTrue(self.blackbox1 == self.blackbox2)
#
#     def test_unequal_1(self):
#         self.blackbox2.listOfROCs[0].pos = Point([10, -11])
#         self.assertFalse(self.blackbox1 == self.blackbox2)
#
#     def test_unequal_2(self):
#         self.blackbox2.listOfROCs[0].rot = 14
#         self.assertFalse(self.blackbox1 == self.blackbox2)
#
#     def test_unequal_3(self):
#         self.blackbox2.listOfROCs.pop()
#         self.blackbox2.numberOfROCs -= 1
#         self.assertFalse(self.blackbox1 == self.blackbox2)
#
# if __name__ == '__main__':
#     unittest.main()

'''
TEST: comparable_Track::__eq__(self, other):
'''
# from TESTS.SPECIFIC_LOGIC.album.auxilary_classes import comparable_Track
# from album import CarRecord, BlackBox
# from point import Point
# import copy
# import unittest
#
# class Test_eq(unittest.TestCase):
#
#     def setUp(self):
#         roc1 = CarRecord()
#         roc1.pos = Point([10, 11])
#         roc1.rot = 12
#         roc1.recordOfRadar.pos = Point([7, 8])
#         roc1.recordOfRadar.rot = 9
#
#         for roran in roc1.recordOfRadar.listOfRORs:
#             roran.pos = Point([1, 2])
#             roran.rot = 3
#             roran.posOfBarrier = Point([4, 5])
#
#         roc2 = copy.deepcopy(roc1)
#         roc3 = copy.deepcopy(roc1)
#
#         blackbox1 = BlackBox()
#         blackbox1.AddCarRecord(roc1)
#         blackbox1.AddCarRecord(roc2)
#
#         blackbox2 = copy.deepcopy(blackbox1)
#         blackbox2.AddCarRecord(roc3)
#
#         self.track1 = comparable_Track()
#         self.track1.AddBlackBox(blackbox1)
#         self.track1.AddBlackBox(blackbox2)
#
#         self.track2 = copy.deepcopy(self.track1)
#
#     def test_equal(self):
#         self.assertEqual(self.track1, self.track2)
#
#     def test_unequal_1(self):
#         self.track1.listOfBlackBoxes[0].listOfROCs[0].rot = 14
#         self.assertNotEqual(self.track1, self.track2)
#
#     def test_unequal_1(self):
#         self.track1.listOfBlackBoxes.pop()
#         self.track1.numberOfBlackBoxes -= 1
#         self.assertNotEqual(self.track1, self.track2)
#
# if __name__ == '__main__':
#     unittest.main()

'''
TEST: comparable_Album::__eq__(self, other):
'''
# from TESTS.SPECIFIC_LOGIC.album.auxilary_classes import comparable_Album
# from album import CarRecord, BlackBox, Track
# from point import Point
# import copy
# import unittest
#
# class Test_eq(unittest.TestCase):
#
#     def setUp(self):
#         roc1 = CarRecord()
#         roc1.pos = Point([10, 11])
#         roc1.rot = 12
#         roc1.recordOfRadar.pos = Point([7, 8])
#         roc1.recordOfRadar.rot = 9
#
#         for roran in roc1.recordOfRadar.listOfRORs:
#             roran.pos = Point([1, 2])
#             roran.rot = 3
#             roran.posOfBarrier = Point([4, 5])
#
#         roc2 = copy.deepcopy(roc1)
#         roc3 = copy.deepcopy(roc1)
#
#         blackbox1 = BlackBox()
#         blackbox1.AddCarRecord(roc1)
#         blackbox1.AddCarRecord(roc2)
#
#         blackbox2 = copy.deepcopy(blackbox1)
#         blackbox2.AddCarRecord(roc3)
#
#         track1 = Track()
#         track1.AddBlackBox(blackbox1)
#         track1.AddBlackBox(blackbox2)
#
#         track2 = copy.deepcopy(track1)
#         track3 = copy.deepcopy(track1)
#
#         self.album1 = comparable_Album()
#         self.album1.AddTrack(track1)
#         self.album1.AddTrack(track2)
#         self.album1.AddTrack(track3)
#
#         self.album2 = copy.deepcopy(self.album1)
#
#
#     def test_equal(self):
#         self.assertEqual(self.album1, self.album2)
#
#     def test_unequal_1(self):
#         self.album1.listOfTracks[0].listOfBlackBoxes[0].listOfROCs[0].rot = 14
#         self.assertNotEqual(self.album1, self.album2)
#
#     def test_unequal_1(self):
#         self.album1.listOfTracks.pop()
#         self.album1.numberOfTracks -= 1
#         self.assertNotEqual(self.album1, self.album2)
#
# if __name__ == '__main__':
#     unittest.main()
