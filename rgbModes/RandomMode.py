from rgbModes.BlankMode import *
import random

#Cylces through the colour using a fading effect.
class RandomMode(Mode):
    
    def __init__(self, controller):
        self.name = "Random"
        self.controller = controller

    def update(self):
        self.controller.setColour(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))