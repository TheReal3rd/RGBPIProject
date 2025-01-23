from Resources.BlankMode import *
from Settings.Setting import *

import time
import math
import colorsys 

class ColourCycleMode(Mode):

    _lastIndex = 0

    def __init__(self):
        self._name = "ColourCycle"
        self._fixtureType = "WSLEDStrip"
        self.settings = [
            Setting("ColourDelay", "Colour cycle delay.", 0.0, float),
            Setting("Brightness", "Sets the Brightness levels.", 255, int),
            Setting("SpreadAmount", "Spread the colour cycle out across the strip.", 10, int),
            Setting("SpreadDelay", "Delay for when the pixel update after preading new colour", 0.01, float)
        ]

    def update(self, fixture):
        for i in range(self._lastIndex, min(self._lastIndex + self.settings[2].getValue(), fixture.getNumPixels())):
            milliseconds = int(round((time.time() + self.settings[0].getValue()) * 1000))
            state = math.ceil(milliseconds / 20)
            state %= 360.0

            colour = colorsys.hsv_to_rgb(float(state / 360.0), 1.0, 1.0)
            r = int( colour[0] * 255 )
            g = int( colour[1] * 255 )
            b = int( colour[2] * 255 )

            fixture.setPixelColour(i, r, g, b, 0)
            fixture.setBrightness(self.settings[1].getValue())

        fixture.show()
        time.sleep(self.settings[3].getValue())
        self._lastIndex += 1

        if self._lastIndex >= fixture.getNumPixels():
            self._lastIndex = 0



        