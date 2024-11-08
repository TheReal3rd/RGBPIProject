from rgbModes.BlankMode import *
from Settings.Setting import *

import random
import time

#Works fine
#Randomly picks a colour using numbers :3
class RandomMode(Mode):

    def __init__(self):
        self._name = "Random"
        self.settings = {
            Setting("Delay", "Delay between colour changes.", 0.25, float),
            Setting("FadingTransition", "Linearly transition to the next colour.", False, bool)
        }

    def update(self):
        time.sleep(self.settings[0].getValue())
        self.controller.setColour(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)