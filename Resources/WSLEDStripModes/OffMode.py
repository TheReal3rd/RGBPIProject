from Resources.BlankMode import *
from Settings.Setting import *
from rpi_ws281x import Color

#Not working irc.
class OffMode(Mode):

    def __init__(self):
        self._name = "Off"
        self._fixtureType = "WSLEDStrip"
        self.settings = []

    def update(self, fixture):
        fixture.wipeColour(0.0005)