from rgbModes.BlankMode import *
import random
import time

#Works fine
#Randomly picks a colour using numbers :3
class RandomMode(Mode):

    def __init__(self, controller):
        self.name = "Random"
        self.controller = controller

    def update(self):
        time.sleep(0.25)
        self.controller.setColour(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)