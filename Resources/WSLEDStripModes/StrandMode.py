from Resources.BlankMode import *
from Settings.Setting import *
import time

#Send a pulse of coloured light along the strip. Not fully working.
class StrandMode(Mode):

    def __init__(self):
        self._name = "Strand"
        self._fixtureType = "WSLEDStrip"
        self.settings = [
            Setting("Brightness", "Sets the Brightness levels.", 255, int)
        ]

    def update(self, fixture):
        pass





        #if not self._finished:
        #    for i in range(fixture.getNumPixels()):
        #        fixture.setPixelColour(i, self.settings[0].getValue(), self.settings[1].getValue(), self.settings[2].getValue(), 0)
        #        fixture.setBrightness(self.settings[3].getValue())
        #    fixture.show()
                 
        #    self._finished = True

        