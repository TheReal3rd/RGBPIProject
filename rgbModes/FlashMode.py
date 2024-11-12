from rgbModes.BlankMode import *
from Settings.Setting import *

from Utils import *

import random
import time

#Works fine
#Flashing colour.
class FlashMode(Mode):
    state = False

    red = 0
    green = 0
    blue = 0

    def __init__(self):
        self._name = "Flash"
        self.settings = [
            Setting("R", "Colour Red", 0, float),
            Setting("G", "Colour Green", 255, float),
            Setting("B", "Colour Blue", 0, float),
            Setting("Bightness", "How bright the colours will be.", 255, float),
            Setting("Delay", "How long to wait to turn off and on the lights.", 0.2, float),
            Setting("SoftTransitions", "Softly flash to the colour.", True, bool),
            Setting("StepSpeed", "The speed it transitions.", 5, float)
        ]

    def update(self):
        toRed = self.settings[0].getValue()
        toGreen = self.settings[1].getValue()
        toBlue = self.settings[2].getValue()

        if self.settings[5].getValue():
            step = self.settings[6].getValue()
            if self.state:
                self.red = moveTowards(self.red, toRed, step)
                self.green = moveTowards(self.green, toGreen, step)
                self.blue = moveTowards(self.blue, toBlue, step)
                if self.red == toRed and self.green == toGreen and self.blue == toBlue:
                    self.state = False
            else:
                self.red = moveTowards(self.red, 0, step)
                self.green = moveTowards(self.green, 0, step)
                self.blue = moveTowards(self.blue, 0, step)
                if self.red == 0 and self.green == 0 and self.blue == 0:
                    self.state = True

            self.controller.setColour(self.red, self.green, self.blue, self.settings[3].getValue())
        else:
            if self.state:
                self.controller.setColour(self.toRed, self.toGreen, self.toBlue, self.settings[3].getValue())
            else: 
                self.controller.setColour(0, 0, 0, 0)
            self.state = not self.state
            time.sleep(self.settings[4].getValue())