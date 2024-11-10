from rgbModes.BlankMode import *
from Settings.Setting import *
from Utils import *

import random
import time

#Works fine
#Randomly picks a colour using random numbers :3
class RandomMode(Mode):


    red = 0
    green = 0
    blue = 0

    toRed = 0
    toGreen = 0
    toBlue = 0

    finished = True    

    def __init__(self):
        self._name = "Random"
        self.settings = [
            Setting("Delay", "Delay between colour changes.", 0.25, float),
            Setting("FadingTransition", "Linearly transition to the next colour.", False, bool)
        ]

    def update(self):
        if self.settings[1].getValue():
            if self.finished:
                self.toRed = random.randint(0, 255)
                self.toGreen = random.randint(0, 255)
                self.toBlue = random.randint(0, 255)
                self.finished = False
            else:
                self.red = moveTowards(self.red, self.toRed, 1)
                self.green = moveTowards(self.red, self.toRed, 1)
                self.blue = moveTowards(self.red, self.toRed, 1)
        else:
            time.sleep(self.settings[0].getValue())
            self.controller.setColour(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)