class AlbumPrinter:
    @classmethod
    def PrintRoran(cls, roran):
        print("               Rangefinder pos:", roran.pos, "rot:", roran.rot, "posOfBarrier:", roran.posOfBarrier)

    @classmethod
    def PrintRorad(cls, rorad):
        print("            Radar ", rorad.pos, rorad.rot)
        for ror in rorad.listOfRORs:
            cls.PrintRoran(ror)

    @classmethod
    def PrintRoc(cls, roc):
        print("         Record no", roc.number, roc.pos, roc.rot)
        cls.PrintRorad(roc.recordOfRadar)

    @classmethod
    def PrintBlackbox(cls, blackbox):
        print("      Blackbox no", blackbox.number)
        for roc in blackbox.listOfROCs:
            cls.PrintRoc(roc)

    @classmethod
    def PrintTrack(cls, track):
        print("   Track no", track.number, "with length:", track.length)
        for blackbox in track.listOfBlackBoxes:
            cls.PrintBlackbox(blackbox)

    @classmethod
    def PrintAlbum(cls, album):
        print("Album")
        for track in album.listOfTracks:
            cls.PrintTrack(track)
