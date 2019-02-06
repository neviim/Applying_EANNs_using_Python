'''
Author: Pawel Brysch
Date: Jan 2019

This script allow you to watch the course of experiment which was performed in multiples steps.
To choose which albums you want to watch you have to write their filenames in "listOfAlbumFilenames" variable at the
beginning of the script. Albums must have correct order.
'''


from Modules.General.general_tools import PathsManager
from Modules.GUI.displayer import Displayer
from Modules.Settings.set_up_manager import SetUpManager
from Modules.Simulation.data_containers import Album
from Modules.Simulation.map import Map

# Set which albums we want to display.
listOfAlbumFilenames = ["album1.txt", "album2.txt"]

# Set up environment
SetUpManager.SetUp()

# Load map
Displayer.map = Map()
Displayer.map.LoadFromFile(PathsManager.GetPath("map"))

# Create list of albums (which will be merged soon).
listOfAlbums = []
for albumFilename in listOfAlbumFilenames:
    album = Album()
    album.LoadFromFile(PathsManager.GetPath("albums", albumFilename))
    listOfAlbums.append(album)

# Merge albums and set as one.
album = Album.MergedAlbums(listOfAlbums)

# Show the course of the experiment.
Displayer.PlayAlbum(album)