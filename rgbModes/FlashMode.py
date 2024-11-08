from rgbModes.BlankMode import *
from Settings.Setting import *

import random
import time

#Works fine
#Flashing colour.
class FlashMode(Mode):
    state = False

    def __init__(self):
        self._name = "Flash"
        self.settings = {
            Setting("R", "Colour Red", 0, float),
            Setting("G", "Colour Green", 255, float),
            Setting("B", "Colour Blue", 0, float),
            Setting("Bightness", "How bright the colours will be.", 255, float),
            Setting("Delay", "How long to wait to turn off and on the lights.", 0.2, float)
        }

    def update(self):
        if self.state:
            self.controller.setColour(settings[0].getValue(), settings[1].getValue(), settings[2].getValue(), 255)
        else: 
            self.controller.setColour(0, 0, 0, 0)
        self.state = not self.state
        time.sleep(settings[4].getValue())