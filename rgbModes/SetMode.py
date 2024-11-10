from rgbModes.BlankMode import *
from Settings.Setting import *

#Set the strip to a solid colour.
class SetMode(Mode):

    def __init__(self):
        self._name = "Set"
        self.settings = [
            Setting("Red", "Sets the Red levels.", 255.0, float),
            Setting("Green", "Sets the Green levels.", 0.0, float),
            Setting("Blue", "Sets the Blue levels.", 0.0, float),
            Setting("Brightness", "Sets the Brightness levels.", 255, float)
        ]

    def update(self):
        self.controller.setColour(self.settings[0].getValue(), self.settings[1].getValue(), self.settings[2].getValue(), self.settings[3].getValue())