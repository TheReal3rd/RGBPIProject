from rgbModes.BlankMode import *
from Settings.Setting import *

from Utils import *

import random
import time
import colorsys

#Works fine
#Flashing colour with colour cycle.
class FlashColourCycleMode(Mode):
    state = False

    rotation = 0
    red = 0
    green = 0
    blue = 0

    toRed = 0
    toGreen = 0
    toBlue = 0


    def __init__(self):
        self._name = "FlashColourCycle"
        self.settings = [
            Setting("Bightness", "How bright the colours will be.", 255, float),
            Setting("StepSpeed", "The speed it transitions.", 5, float),
            Setting("CycleSpeed", "The cycle speed colour transitions.", 25, float)
        ]

    def update(self):
        step = self.settings[1].getValue()
        if self.state:
            self.red = moveTowards(self.red, self.toRed, step)
            self.green = moveTowards(self.green, self.toGreen, step)
            self.blue = moveTowards(self.blue, self.toBlue, step)
            if self.red == self.toRed and self.green == self.toGreen and self.blue == self.toBlue:
                self.state = False

        else:
            if not (self.red == 0 and self.green == 0 and self.blue == 0):
                self.red = moveTowards(self.red, 0, step)
                self.green = moveTowards(self.green, 0, step)
                self.blue = moveTowards(self.blue, 0, step)

            else:

                colour = colorsys.hsv_to_rgb(float(self.rotation / 360.0), 1.0, 1.0)
                self.toRed = colour[0] * 255
                self.toGreen = colour[1] * 255
                self.toBlue = colour[2] * 255
                self.rotation += self.settings[2].getValue()
                if self.rotation >= 360.0:
                    self.rotation = 0

                self.state = True

        self.controller.setColour(self.red, self.green, self.blue, self.settings[1].getValue())