from Resources.LEDStripModes.BlankMode import *
from Settings.Setting import *

#Simply do nothing. ez But yea found using None and handling the user of None each time waste time. So thats why this mode exists.
class OffMode(Mode):

    def __init__(self):
        self._name = "Off"
        self.settings = []

    def update(self):
        self.controller.setColour(0, 0, 0, 0)