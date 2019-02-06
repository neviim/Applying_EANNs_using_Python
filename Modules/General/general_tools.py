''' GENERAL TOOLS
Author: Pawel Brysch
Date: Jan 2019

Module contains classes which execute basic operations. Purpose of this module was to improve style of code.
Classes are not connected which each other.
'''


import os
import pygame as pg
from Modules.Simulation.geometry import Vector


class PathsManager:
    ''' Using this class allow you to contain all paths you need in your project in one easily accessible place.

    ...
    Attributes
    ----------
    mainPath: str
        project path. To be set in external module (e.q. settings).
    files: dict
        contains paths to the files you need
    directories: dict
        contains paths to the directories you need. It is better choice for directories with dynamically changing
        content.
    '''
    mainPath = None
    files = {}
    directories = {}

    @classmethod
    def AddFile(cls, key, relativePath):
        '''
        :param key: str
            name under which you will get your path.
        :param relativePath: str
            path, which begins in your project directory
        '''
        cls.files[key] = cls.mainPath + relativePath

    @classmethod
    def AddDirectory(cls, key, relativePath):
        '''
        :param key: str
            name under which you will get your path
        :param relativePath: str
            path, which begins in your project directory
        '''
        cls.directories[key] = cls.mainPath + relativePath

    @classmethod
    def GetPath(cls, key, filename=None):
        ''' You can use this method in two ways.
        1. If you want to get saved file's path, pass file's key as "key" and don't pass "filename" argument.
        2. If you want to get file path from saved directory's path, pass directory's key as "key" and file's name as
        "filename".

        :param key: str
            name of file or directory.
        :param filename: str
            full filename, e.q. "something.txt". Should exist in chosen directory.
        '''

        if filename is None:
            return cls.files[key]
        else:
            return cls.directories[key] + filename

class ImagesManager:
    ''' This class allow you to store and transform images you need in your project.
        IMPORTANT! Method "Initialize" must be executed before proper using of this class.

    ...
    Attributes
    ----------
    images: dict
        contains all images you need in your project
    '''
    images = {}

    @classmethod
    def Initialize(cls):
        '''  Graphics engine, that we use, is Pygame. It requires using line below to works properly.
        '''
        pg.display.set_mode((1, 1))

    @classmethod
    def AddImage(cls, key, path, scale=1):
        ''' Method that allows you to add image and scale it (optionally).

        :param key: str
            name under which you will get your image
        :param path: str
            full path to image
        :param scale: float
        '''

        if scale == 1:
            cls.images[key] = pg.image.load(path).convert_alpha()
        else:
            cls.images[key] = cls.scaledImage(pg.image.load(path).convert_alpha(), scale)

    @classmethod
    def GetImage(cls, key):
        ''' Get image by passing its key.

        :param key: str
            name of image
        :return: Pygame.Image
        '''
        return cls.images[key]

    @classmethod
    def scaledImage(cls, image, scale):
        ''' Scale image

        :param image: Pygame.Image
        :param scale: float or Vector
        :return: Pygame.Image
        '''

        # We can scale in two dimensions. Statements below solves problem when "scale" argument was passed as single
        # float. In that case, we scale image in two dimensions keeping the proportions.
        try:
            scale[0]
        except TypeError:
            scale = Vector(scale, scale)

        newSize = Vector(image.get_rect().size).ScaledByVector(scale)
        return pg.transform.scale(image, newSize.asInt())

    @classmethod
    def rotatedImage(cls, image, rot):
        ''' Rotate image

        :param image: Pygame.Image
        :param rot: float
        :return: Pygame.Image
        '''
        return pg.transform.rotate(image, rot)

    @classmethod
    def transformedImage(cls, image, scale, rot):
        ''' Scale and rotate image at once.

        :param image: Pygame.Image
        :param scale: float or Vector
        :param rot: float
        :return: Pygame.Image
        '''
        intermediateImage = cls.scaledImage(image, scale)
        return cls.rotatedImage(intermediateImage, rot)


class FilesManager:
    ''' Class contains set of methods. The purpose is to handle files in more good-looking way.
    '''
    @classmethod
    def LinesFromFile(cls, filename):
        '''
        :param filename: str
            full path
        :return: list
            list of strings, where each string is one line in the file. Order has been preserved.
        '''
        with open(filename, 'rt') as file:
            lines = file.readlines()
            return lines

    @classmethod
    def AddLineToFile(cls, line, filename):
        ''' Useful when we are writing in one file from many different places in the code.

        :param line: str
        :param filename: str
            full path
        '''
        with open(filename, "a") as file:
            file.write(line + "\n")
            file.close()

    @classmethod
    def ClearFile(cls, filename):
        ''' Clear chosen file.

        :param filename: str
            full path
        '''
        file = open(filename, "w")
        file.close()


class BuiltInTypesConverter:
    ''' Set of converting methods when arguments are not single, but whole lists.
    '''
    @classmethod
    def StringToInts(cls, line):
        '''
        :param line: str
            contains numbers
        :return: list
            list of integers
        '''

        return [int(element) for element in line.split()]

    @classmethod
    def StringToFloats(cls, string):
        '''
        :param string: str
            contains numbers
        :return: floats
            list of floating numbers
        '''

        return [float(element) for element in string.split()]

    @classmethod
    def IntsToString(cls, ints):
        '''
        :param ints: list
            list of integers
        :return: str
            contains numbers
        '''

        result = ""
        for element in ints:
            result = result + str(int(element)) + " "
        return result

    @classmethod
    def FloatsToString(cls, floats):
        '''
        :param floats: list
            list of floating numbers
        :return: str
            contains numbers
        '''

        result = ""
        for element in floats:
            result = result + str(element) + " "
        return result

