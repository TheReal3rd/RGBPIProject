from rgbModes.BlankMode import *
import random
import time

#Works fine
#Randomly picks a colour using numbers :3
class TestMode(Mode):
    state = False

    def __init__(self, controller):
        self.name = "Test1"
        self.controller = controller

    def update(self):
        if self.state:
            self.controller.setColour(255, 0, 0, 0)
        else: 
            self.controller.setColour(255, 0, 0, 255)
        time.sleep(0.01)