'''
TEST Displayer::PlayAlbum(self)
'''
from Modules.GUI.displayer import Displayer
from Modules.Simulation.map import Map
from Modules.General.general_tools import PathsManager
from Modules.Simulation.data_containers import Album
from Modules.Settings.set_up_manager import SetUpManager

import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)

SetUpManager.SetUp()

amap = Map()
amap.LoadFromFile(PathsManager.GetPath("map"))
adisplayer = Displayer
adisplayer.map = amap
album = Album()
album.LoadFromFile(PathsManager.GetPath("albums", "album1.txt"))
adisplayer.PlayAlbum(album)


