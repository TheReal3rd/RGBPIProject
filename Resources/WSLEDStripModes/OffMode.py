from Resources.BlankMode import *
from Settings.Setting import *

#Not working irc.
class OffMode(Mode):

    def __init__(self):
        self._name = "Off"
        self._fixtureType = "WSLEDStrip"
        self.settings = []

    def update(self, fixture):
        fixture.wipeColour()