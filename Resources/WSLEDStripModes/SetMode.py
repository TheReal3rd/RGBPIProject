from Resources.BlankMode import *
from Settings.Setting import *
from rpi_ws281x import Color
import time

#Set the strip to a solid colour.
class SetMode(Mode):

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
        for i in range(fixture.getStrip().numPixels()):
            fixture.setPixelColor(i, self.settings[0].getValue(), self.settings[1].getValue(), self.settings[2].getValue(), 0)
        fixture.getStrip().setBrightness(self.settings[3].getValue())
        fixture.getStrip().show()
        time.sleep(10 / 1000)
        