from Resources.BlankMode import *
from Settings.Setting import *
from rpi_ws281x import Color

#Set the strip to a solid colour.
class SetMode(Mode):

    def __init__(self):
        self._name = "Set"
        self._fixtureType = "WSLEDStrip"
        self.settings = [
            Setting("Red", "Sets the Red levels.", 255.0, float),
            Setting("Green", "Sets the Green levels.", 0.0, float),
            Setting("Blue", "Sets the Blue levels.", 0.0, float),
            Setting("Brightness", "Sets the Brightness levels.", 255, float)
        ]

    def update(self, fixture):
        for i in range(fixture.getStrip().numPixels()):
            fixture.getStrip().setPixelColor(i, Color(self.settings[0].getValue(), self.settings[1].getValue(), self.settings[2].getValue()))
        fixture.setBrightness(self.setting[3].getValue())
        fixture.getStrip().show()
        