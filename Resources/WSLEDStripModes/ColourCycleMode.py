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
            Setting("ColourDelay", "Colour cycle delay.", 0.0, float),
            Setting("Brightness", "Sets the Brightness levels.", 255, int)
        ]

    def update(self, fixture):#Not done yet TODO
        pass
        