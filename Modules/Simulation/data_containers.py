''' DATA CONTAINERS
Author: Pawel Brysch
Date: Jan 2019

Module contains classes which are used to create containers for data generated during learning process.
They have a hierarchy, which can be explained as below:

    Album object can contain many Track objects,
    Track object can contain many BlackBox objects,
    BlackBox can contain many CarRecord objects,
    CarRecord contains RadarRecord object,
    RadarRecord object contains RangefinderRecord objects (usually fixed number).

Each of class's representatives can be separately saved to file, but only Album can be loaded from file. In other cases
we can only load object from list of strings. The reason of this situation is that for typical purposes we use save/load
methods only for "Album" objects.

These containers don't contain all data about learning process. E.q. they don't have any information about wages in neu-
ral networks. Using them, you could only see what happened from 'spectator' perspective. In other worlds, they store in-
formation only about 'physical' aspects of simulation.
'''

from Modules.General.general_tools import FilesManager, BuiltInTypesConverter
from Modules.Simulation.geometry import Point




class RangefinderRecord:
    '''
    Object of this class contains data about rangefinder in one specific moment. One record is usually assigned to one
    rangefinder and is used only for one moment in that rangefinder's lifecycle.

    ...

    Attributes
    ----------
    pos: Point
        position of rangefinder
    rot: float
        rotation of rangefinder
    posOfBarrier: Point
        point when ray from rangefinder falls on environment
    '''
    def __init__(self):
        self.pos = Point()
        self.rot = None
        self._posOfBarrier = Point()

    @property
    def posOfBarrier(self):
        return self._posOfBarrier

    @posOfBarrier.setter
    def posOfBarrier(self, value):
        if value is not None:
            self._posOfBarrier = value
        else:
            self._posOfBarrier = Point([0, 0])

    def SaveToFile(self, filename):
        ''' Save object's parameters in specific order.
        '''
        listOfData = [self.pos[0], self.pos[1], self.rot, self.posOfBarrier[0], self.posOfBarrier[1]]
        FilesManager.AddLineToFile(BuiltInTypesConverter.IntsToString(listOfData), filename)

    def LoadFromLine(self, line):
        ''' Helper function, used only in RadarRecord.LoadFromLines()

        :param line: str
            string which contains data about rangefinder in specific order
        '''
        self.pos.x, self.pos.y, self.rot, self.posOfBarrier.x, self.posOfBarrier.y = BuiltInTypesConverter.StringToInts(line)




class RadarRecord:
    '''
    Object of this class contains data about radar in one specific moment. One record is usually assigned to one
    radar and is used only for one moment in that radar's lifecycle.

    ...
    Attributes
    ----------
    numberOfRangefinderRecords: int
        class attribute. In one experiment all radar should have same number of rangefinders
        To be set in external module (e.q. settings).
    pos: Point
        position of radar
    rot: float
        rotation of radar
    listOfRangefinderRecords:
        length of this list is typically fixed in one experiment
    '''
    numberOfRangefinderRecords = None

    def __init__(self, listOfRangefinders=None):
        self.pos = Point()
        self.rot = None
        self.listOfRangefinderRecords = [RangefinderRecord()] * self.__class__.numberOfRangefinderRecords

        if listOfRangefinders is not None:
            for _ in range(self.__class__.numberOfRangefinderRecords):
                self.listOfRangefinderRecords[_] = listOfRangefinders[_].record

    def SaveToFile(self, filename):
        ''' Save object's parameters in specific order.
        '''

        #Save data about radar exclusively
        with open(filename, "a") as file:
            listOfData = [self.pos[0], self.pos[1], self.rot]
            file.write(BuiltInTypesConverter.IntsToString(listOfData) + "\n")

        #Save data about rangefinders
        for rangefinderRecord in self.listOfRangefinderRecords:
            rangefinderRecord.SaveToFile(filename)

    def LoadFromLines(self, lines):
        ''' Helper function, used only in CarRecord.LoadFromLines()

        :param lines: list
            list of strings which contains data about radar in specific order
        '''
        first_line, rest = lines[0], lines[1:]

        # Load data about radar exclusively
        self.pos.x, self.pos.y, self.rot = BuiltInTypesConverter.StringToInts(first_line)

        # Load data about rangefinders
        for _, line in zip(range(self.__class__.numberOfRangefinderRecords), rest):
            rangefinderRecord = RangefinderRecord()
            rangefinderRecord.LoadFromLine(line)
            self.listOfRangefinderRecords[_] = rangefinderRecord




class CarRecord:
    '''
    Object of this class contains data about car in one specific moment. One record is usually assigned to one
    car and is used only for one moment in that car's lifecycle.

    ...

    Attributes
    ----------

    pos: Point
        position of car
    rot: float
        rotation of car
    radarRecord: RadarRecord
    number: int
        object number in black box which contains that objects. It has possibility to improve efficiency of algorithms
        implemented in future.
    '''
    def __init__(self, radarRecord=None):
        self.pos = Point()
        self.rot = None

        if radarRecord is None:
            self.radarRecord = RadarRecord()
        else:
            self.radarRecord = radarRecord

        self.number = None

    def SaveToFile(self, filename):
        ''' Save object's parameters in specific order
        '''

        # Save data about car exclusively
        with open(filename, "a") as file:
            listOfData = [self.pos[0], self.pos[1], self.rot]
            file.write(BuiltInTypesConverter.IntsToString(listOfData) + "\n")

        # Save data about radar
        self.radarRecord.SaveToFile(filename)

    def LoadFromLines(self, lines):
        ''' Helper function, used only in "BlackBox.LoadFromLines()"

        :param line: list
            list of strings which contains data about car in specific order
        '''

        first_line, rest = lines[0], lines[1:]

        # Load data about car exclusively
        self.pos.x, self.pos.y, self.rot = BuiltInTypesConverter.StringToInts(first_line)

        # Load data about radar
        self.radarRecord.LoadFromLines(rest)

class BlackBox:
    ''' Object of this class contains all data about car from it's whole lifecycle.

    ...
    Attributes
    ----------
    listOfCarRecords: list
    number: int
        object's number in track which contains that objects. It has possibility to improve efficiency of algorithms
        implemented in future
    numberOfCarRecords: int
        Property used to decorate length of "listOfCarRecords"
    '''
    def __init__(self):
        self.listOfCarRecords = []
        self.number = None

    @property
    def numberOfCarRecords(self):
        return None

    @numberOfCarRecords.getter
    def numberOfCarRecords(self):
        return len(self.listOfCarRecords)

    def AddCarRecord(self, carRecord):
        ''' Augmented listOfCarRecords.append().
        '''
        carRecord.number = self.numberOfCarRecords
        self.listOfCarRecords.append(carRecord)


    def SaveToFile(self, filename):
        ''' Save object's parameters in specific order
        '''

        # Line which we writing using code below will be usable during loading process
        with open(filename, "a") as file:
            file.write(str(self.numberOfCarRecords) + "\n")

        # Save records
        for roc in self.listOfCarRecords:
            roc.SaveToFile(filename)

    def LoadFromLines(self, lines):
        ''' Helper function, used only in "Track.LoadFromLines()"

        :param line: list
            list of strings. List is divided into parts referring to corresponding car records.
        '''
        first_line, rest = lines[0], lines[1:]

        numberOfCarRecords = BuiltInTypesConverter.StringToInts(first_line)[0]
        linesPerSingleCarRecord = int(len(rest)/numberOfCarRecords)

        #Read one car record per single iteration
        while len(rest) >= 1:
            carRecord = CarRecord()
            carRecord.LoadFromLines(rest[:linesPerSingleCarRecord])
            self.AddCarRecord(carRecord)

            #Remove already read data from rest of data to read.
            rest = rest[linesPerSingleCarRecord:]




class Track:
    ''' Object of this class contains data about single generation of cars.

    ...
    Attributes
    ----------
    listOfBlackboxes: list
    length: int
        length of longest black box in "listOfBlackBoxes"
    number: int
        object's number in album which contains that objects. It has possibility to improve efficiency of algorhithms
        implemented in future
    numberOfBlackBoxes: int
        Property used to decorate length of listOfBlackBoxes
    '''
    def __init__(self):
        self.listOfBlackBoxes = []
        self.length = 0
        self.number = None

    @property
    def numberOfBlackBoxes(self):
        return None

    @numberOfBlackBoxes.getter
    def numberOfBlackBoxes(self):
        return len(self.listOfBlackBoxes)

    def AddBlackBox(self, blackBox):
        ''' Augmented "listOfBlackBoxes.append".
        '''

        blackBox.number = self.numberOfBlackBoxes
        self.listOfBlackBoxes.append(blackBox)
        self.RevaluateLength(len(blackBox.listOfCarRecords))


    def RevaluateLength(self, potentialNewLength):
        ''' Update "length" attribute
        '''

        if potentialNewLength > self.length:
            self.length = potentialNewLength

    def SaveToFile(self, filename):
        ''' Save object
        '''

        with open(filename, "a") as file:

            # Lines which we writing using code below will be usable during loading process
            numberOfCarRecords = sum([len(blackbox.listOfCarRecords) for blackbox in self.listOfBlackBoxes])
            linesPerSingleCarRecord = RadarRecord.numberOfRangefinderRecords+2
            file.write(str(linesPerSingleCarRecord)+" "+str(numberOfCarRecords)+"\n")

        #Save black boxes
        for blackbox in self.listOfBlackBoxes:
            blackbox.SaveToFile(filename)

    def LoadFromLines(self, lines):
        ''' Helper function, used only in "Album.LoadFromLines"

        :param line: list
            list of strings. List is divided into parts referring to corresponding black boxes.
        '''
        first_line, rest = lines[0], lines[1:]

        linesPerSingleCarRecord = BuiltInTypesConverter.StringToInts(first_line)[0]

        # Read one black box record per single iteration
        while len(rest) >= 1:
            numberOfCarRecordsInNextBlackBox = BuiltInTypesConverter.StringToInts(rest[0])[0]

            # Comment: " + 1" on the end of next line of code results from fact, that black box need one additional line
            # with information which are necessary to properly loading.
            numberOfLinesForNextBlackBox = numberOfCarRecordsInNextBlackBox * linesPerSingleCarRecord + 1
            blackbox = BlackBox()
            blackbox.LoadFromLines(rest[:numberOfLinesForNextBlackBox])
            self.AddBlackBox(blackbox)

            # Remove already read data from rest of data to read.
            rest = rest[numberOfLinesForNextBlackBox:]

class Album:
    ''' Object of this class contains data about all generations of cars in single experiment

    ...
    Attributes
    ----------
    listOfTracks:
    numberOfTracks: int
        Property used to decorate length of "listOfTracks"
    '''
    def __init__(self):
        self.listOfTracks = []

    @property
    def numberOfTracks(self):
        return None

    @numberOfTracks.getter
    def numberOfTracks(self):
        return len(self.listOfTracks)


    def AddTrack(self, track):
        ''' Augmented "listOfBlackBoxes.append".
        '''
        track.number = self.numberOfTracks
        self.listOfTracks.append(track)


    def SaveToFile(self, filename):
        ''' Save object
        '''

        #Clear the file
        file0 = open(filename, "w")
        file0.close()

        with open(filename, "a") as file:
            # Lines which we writing using code below will be usable during loading process
            linesPerSingleCarRecord = RadarRecord.numberOfRangefinderRecords+2
            blackboxesPerTrack = len(self.listOfTracks[0].listOfBlackBoxes)
            file.write(str(linesPerSingleCarRecord)+" "+str(blackboxesPerTrack)+"\n")

        #Save tracks
        for track in self.listOfTracks:
            track.SaveToFile(filename)

    def LoadFromLines(self, lines):
        ''' Helper function, used only in "Album.LoadFromFile"

        :param line: list
            list of strings. List is divided into parts referring to corresponding tracks.
        '''
        first_line, rest = lines[0], lines[1:]

        linesPerSingleCarRecord, blackboxesPerTrack = BuiltInTypesConverter.StringToInts(first_line)

        # Read one track record per single iteration
        while len(rest) >= 1:
            firstLineFromNextTrack = rest[0]
            numberOfRocsInNextTrack = BuiltInTypesConverter.StringToInts(firstLineFromNextTrack)[1]

            # Comment about line below:
            # " + blackboxesPerTrack" results from fact, that black box need one additional line with information which
            # are necessary for properly loading. We have "blackboxesPerTrack" black boxes in next track, so that
            # addition.
            # " + 1" results from fact, that track also requires one additional line.
            numberOfLinesForNextTrack = linesPerSingleCarRecord * numberOfRocsInNextTrack + blackboxesPerTrack + 1
            track = Track()
            track.LoadFromLines(rest[:numberOfLinesForNextTrack])
            self.AddTrack(track)

            # Remove already read data from rest of data to read.
            rest = rest[numberOfLinesForNextTrack:]

    def LoadFromFile(self, filename):
        ''' Load album from file
        '''

        file = open(filename, "r")
        lines = file.readlines()
        self.LoadFromLines(lines)
        file.close()


    @classmethod
    def MergedAlbums(cls, listOfAlbums):
        ''' Sum of albums which are given in list.
        The order matters. We add albums in the same way as we concatenate strings. All usable parameters (as numbers
        required to some algorithms are calculated as if album was created entirely at once.

        These method allow divide your experiment to stages.

        :param listOfAlbums:
        :return: Album
        '''

        result = Album()
        for album in listOfAlbums:
            for track in album.listOfTracks:
                result.AddTrack(track)
        return result
