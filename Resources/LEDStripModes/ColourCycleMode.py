from Resources.LEDStripModes.BlankMode import *
from Settings.Setting import *

import math
import time
import colorsys # https://davis.lbl.gov/Manuals/PYTHON/library/colorsys.html

#Perfect!
#Cycles through the colours with no black.
class FadingCycleMode(Mode):
    brightness = 255.0
    r = 0.0
    g = 0.0
    b = 0.0

    def __init__(self):
        self._name = "ColourCycle"
        self.settings = [
            Setting("Delay", "Delay between colour changes.", 0.0, float),
            Setting("Brightness", "Brightness of the LED.", 255.0, float)
        ]

    def update(self, fixture):
        milliseconds = int(round((time.time() + self.settings[0].getValue()) * 1000))
        state = math.ceil(milliseconds / 20)
        state %= 360.0

        colour = colorsys.hsv_to_rgb(float(state / 360.0), 1.0, 1.0)
        self.r = colour[0] * 255
        self.g = colour[1] * 255
        self.b = colour[2] * 255

        fixture.setColour(self.r, self.g, self.b, self.settings[1].getValue())