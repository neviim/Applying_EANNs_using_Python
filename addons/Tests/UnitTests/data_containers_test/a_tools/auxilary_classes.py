import random
from Modules.Simulation.data_containers import RangefinderRecord, RadarRecord, CarRecord, BlackBox, Track, Album
from Modules.Simulation.geometry import Point

def random_int():
    return random.randint(-200, 200)

def upgradeAttribute(attributeName, object, newClass):
    newValue = newClass()
    if getattr(object, attributeName) is not None:
        newValue.__dict__ = getattr(object, attributeName).__dict__.copy()
    setattr(object, attributeName, newValue)

def upgradeElements(list0, newClass):
    for index in range(len(list0)):
        newValue = newClass()
        newValue.__dict__ = list0[index].__dict__.copy()
        list0[index] = newValue


class comparable_RecordOfRangefinder(RangefinderRecord):
    def __init__(self):
        super(comparable_RecordOfRangefinder, self).__init__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

class random_RecordOfRangefinder(comparable_RecordOfRangefinder):
    def __init__(self):
        super(random_RecordOfRangefinder, self).__init__()
        self.pos = Point([random_int(), random_int()])
        self.rot = random_int()
        self.posOfBarrier = Point([random_int(), random_int()])


class comparable_RecordOfRadar(RadarRecord):
    def __init__(self):
        super(comparable_RecordOfRadar, self).__init__()

    def __eq__(self, other):
        result = self.pos == other.pos and self.rot == other.rot
        try:
            for self_ror, other_ror in zip(self.listOfRangefinderRecords, other.listOfRangefinderRecords):
                if self_ror.__dict__ != other_ror.__dict__:
                    result = False
        except:
            result = False
        return result

class random_RecordOfRadar(comparable_RecordOfRadar):
    def __init__(self):
        super(random_RecordOfRadar, self).__init__()
        self.pos = Point([random_int(), random_int()])
        self.rot = random_int()

        for index in range(len(self.listOfRangefinderRecords)):
            self.listOfRangefinderRecords[index] = random_RecordOfRangefinder()

class comparable_RecordOfCar(CarRecord):
    def __init__(self):
        super(comparable_RecordOfCar, self).__init__()

    def __eq__(self, other):
        result = self.pos == other.pos and self.rot == other.rot
        try:
            upgradeAttribute("radarRecord", self, comparable_RecordOfRadar)
            upgradeAttribute("radarRecord", other, comparable_RecordOfRadar)
            if self.radarRecord != other.radarRecord:
                result = False
        except:
            result = False
        return result

    def Create(self, other):
        self.__dict__ = other.__dict__


class random_RecordOfCar(comparable_RecordOfCar):
    def __init__(self):
        super(random_RecordOfCar, self).__init__()
        self.pos = Point([random_int(), random_int()])
        self.rot = random_int()
        self.radarRecord = random_RecordOfRadar()

class comparable_BlackBox(BlackBox):
    def __init__(self):
        super(comparable_BlackBox, self).__init__()

    def __eq__(self, other):
        result = self.numberOfCarRecords == other.numberOfCarRecords
        try:
            upgradeElements(self.listOfCarRecords, comparable_RecordOfCar)
            upgradeElements(other.listOfCarRecords, comparable_RecordOfCar)
            for self_roc, other_roc in zip(self.listOfCarRecords, other.listOfCarRecords):
                if self_roc != other_roc:
                    result = False
        except:
            result = False

        return result

class random_BlackBox(comparable_BlackBox):
    def __init__(self, numberOfRocs):
        super(comparable_BlackBox, self).__init__()
        self.listOfCarRecords = [random_RecordOfCar() for i in range(numberOfRocs)]
        # self.numberOfCarRecords = numberOfRocs


class comparable_Track(Track):
    def __init__(self):
        super(comparable_Track, self).__init__()

    def __eq__(self, other):
        result = self.numberOfBlackBoxes == other.numberOfBlackBoxes
        try:
            upgradeElements(self.listOfBlackBoxes, comparable_BlackBox)
            upgradeElements(other.listOfBlackBoxes, comparable_BlackBox)
            for self_blackbox, other_blackbox in zip(self.listOfBlackBoxes, other.listOfBlackBoxes):
                if self_blackbox != other_blackbox:
                    result = False
        except:
            result = False

        return result

class random_Track(comparable_Track):
    def __init__(self, numberOfBlackboxes, rocsPerBlackBox):
        super(random_Track, self).__init__()
        self.listOfBlackBoxes = [random_BlackBox(rocsPerBlackBox) for i in range(numberOfBlackboxes)]
        # self.numberOfBlackBoxes = numberOfBlackboxes

class comparable_Album(Album):
    def __init__(self):
        super(comparable_Album, self).__init__()

    def __eq__(self, other):
        result = self.numberOfTracks == other.numberOfTracks
        try:
            upgradeElements(self.listOfTracks, comparable_Track)
            upgradeElements(other.listOfTracks, comparable_Track)
            for self_track, other_track in zip(self.listOfTracks, other.listOfTracks):
                if self_track != other_track:
                    result = False
        except:
            result = False

        return result

class random_Album(comparable_Album):
    def __init__(self, numberOfTracks, blackboxesPerTrack, rocsPerBlackBox):
        super(random_Album, self).__init__()
        self.listOfTracks = [random_Track(blackboxesPerTrack, rocsPerBlackBox) for i in range(numberOfTracks)]
        # self.numberOfTracks = numberOfTracks

