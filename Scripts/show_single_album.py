'''
Author: Pawel Brysch
Date: Jan 2019

This script allow you to watch the course of chosen experiment.
To choose which album you want to watch you have to save its filename in "albumFilename" variable at the beginning of
the script.
'''
from Modules.General.general_tools import PathsManager
from Modules.GUI.displayer import Displayer
from Modules.Settings.set_up_manager import SetUpManager
from Modules.Simulation.data_containers import Album
from Modules.Simulation.map import Map

# Set which album we want to display.
albumFilename = "album1.txt"

# Set up environment
SetUpManager.SetUp()

# Load map
Displayer.map = Map()
Displayer.map.LoadFromFile(PathsManager.GetPath("map"))

# Load album to display.
album = Album()
album.LoadFromFile(PathsManager.GetPath("albums", albumFilename))

# Show the course of the experiment.
Displayer.PlayAlbum(album)