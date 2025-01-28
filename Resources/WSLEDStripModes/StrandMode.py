from Resources.BlankMode import *
from Settings.Setting import *
import time

#Send a pulse of coloured light along the strip. Not fully working.
class StrandMode(Mode):

    _indexOffset: int = -1
    _finished: bool = False

    def __init__(self):
        self._name = "Strand"
        self._fixtureType = "WSLEDStrip"
        self.settings = [
            Setting("Brightness", "Sets the Brightness levels.", 255, int),
            Setting("Width", "The lighting blob size.", 5, int)
        ]
        self._indexOffset = 0
        self._finished = False

    def update(self, fixture):
        if not self._finished:
            for i in range(fixture.getNumPixels()):
                fixture.setPixelColour(i, 0, 0, 0, 0)
                fixture.setBrightness(255)

            for i in range(self._indexOffset, clamp(self._indexOffset + self.settings[1].getValue(), 0, fixture.getNumPixels())):
                fixture.setPixelColour(i, 255,255,255, 0)
                fixture.setBrightness(255)
            fixture.show()
                 
            self._finished = True

        if self._finished:
            self._indexOffset += 1
            if self._indexOffset >= fixture.getNumPixels():
                self._indexOffset = 0
            self._finished = False

        