from Resources.BlankMode import *
from Settings.Setting import *
import time

#Set the strip to a solid colour. Not fully working.
class SetMode(Mode):

    _finished = False

    def __init__(self):
        self._name = "Set"
        self._fixtureType = "WSLEDStrip"
        self.settings = [
            Setting("Red", "Sets the Red levels.", 255, int),
            Setting("Green", "Sets the Green levels.", 0, int),
            Setting("Blue", "Sets the Blue levels.", 0, int),
            Setting("Brightness", "Sets the Brightness levels.", 255, int)
        ]

    def update(self, fixture):
        if not self._finished:
            for i in range(fixture.getNumPixels()):
                fixture.setPixelColour(i, self.settings[0].getValue(), self.settings[1].getValue(), self.settings[2].getValue(), 0)
                fixture.setBrightness(self.settings[3].getValue())
            fixture.show()
                 
            self._finished = True

    def onSettingChange(self, fixture, settings):
        self._finished = False
        