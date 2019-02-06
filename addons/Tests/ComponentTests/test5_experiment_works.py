from Modules.AI.Genetics.genetics import AlbumWriter, EvolutonaryAlgorithm
from Modules.GUI.displayer import Displayer
from Modules.Simulation.map import Map
from Modules.General.general_tools import PathsManager
from Modules.Settings.set_up_manager import SetUpManager
from Modules.Settings.settings import SETTINGS


#SETUP
SetUpManager.SetUp()

EvolutonaryAlgorithm.Execute()

amap = Map()
amap.LoadFromFile(PathsManager.GetPath("map"))
adisplayer = Displayer
adisplayer.map = amap

albumWriter = AlbumWriter()
album = albumWriter.AlbumFromAlgorithm(EvolutonaryAlgorithm)
adisplayer.PlayAlbum(album)
