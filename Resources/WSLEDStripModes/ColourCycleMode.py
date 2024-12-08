from Resources.BlankMode import *
from Settings.Setting import *
from rpi_ws281x import Color

import time
import random

class ColourCycleMode(Mode):

    def __init__(self):
        self._name = "ColourCycle"
        self._fixtureType = "WSLEDStrip"
        self.settings = [
            Setting("ColourDelay", "Colour cycle delay.", random.randrange(0.0, 0.9), float),
            Setting("Brightness", "Sets the Brightness levels.", 255, int)
        ]

    def update(self, fixture):#Not done yet TODO
        for i in range(fixture.getStrip().numPixels()):
            fixture.setPixelColor(i, self.settings[0].getValue(), self.settings[1].getValue(), self.settings[2].getValue(), 0)
            fixture.getStrip().setBrightness(self.settings[3].getValue())
            fixture.getStrip().show()
            time.sleep(10 / 1000)
        