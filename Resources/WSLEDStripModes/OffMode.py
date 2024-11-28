from Resources.BlankMode import *
from Settings.Setting import *
from rpi_ws281x import Color

#Simply do nothing. ez But yea found using None and handling the user of None each time waste time. So thats why this mode exists.
class OffMode(Mode):

    def __init__(self):
        self._name = "Off"
        self._fixtureType = "WSLEDStrip"
        self.settings = []

    def update(self, fixture):
        for i in range(fixture.getStrip().numPixels()):
            fixture.getStrip().setPixelColor(i, Color(0,0,0,0))
        fixture.setBrightness(0)
        fixture.getStrip().show()