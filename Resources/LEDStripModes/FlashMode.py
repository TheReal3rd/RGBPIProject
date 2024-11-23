from Resources.LEDStripModes.BlankMode import *
from Settings.Setting import *

from Resources.Utils import *

import random
import time

#Works fine
#Flashing colour.
#Technically wrong as it should use brightness but i like the effect it gives so im keeping it.
class FlashMode(Mode):
    state = False

    brightness = 255
    red = 0
    green = 0
    blue = 0

    def __init__(self):
        self._name = "Flash"
        self.settings = [
            Setting("R", "Colour Red", 0, float),#1
            Setting("G", "Colour Green", 255, float),#2
            Setting("B", "Colour Blue", 0, float),#3
            Setting("Bightness", "How bright the colours will be.", 255, float),#4
            Setting("Delay", "How long to wait to turn off and on the lights.", 0.2, float),#5
            Setting("SoftTransitions", "Softly flash to the colour.", True, bool),#6
            Setting("StepSpeed", "The speed it transitions.", 5, float),#7
            Setting("UseBrightness", "When using Soft Transitions instead of fading colour out fade brightness.", True, bool)#8
        ]

    def update(self, fixture):
        toRed = self.settings[0].getValue()
        toGreen = self.settings[1].getValue()
        toBlue = self.settings[2].getValue()

        if self.settings[5].getValue():
            step = self.settings[6].getValue()
            if self.settings[7].getValue():
                self.red = toRed
                self.green = toGreen
                self.blue = toBlue
                if self.state:
                    toBrightness = self.settings[3].getValue()
                    self.brightness = moveTowards(self.brightness, toBrightness, step)
                    if self.brightness == toBrightness:
                        self.state = False
                else:
                    self.brightness = moveTowards(self.brightness, 0, step)
                    if self.brightness == 0:
                        self.state = True

                self.controller.setColour(self.red, self.green, self.blue, self.brightness)
            else:
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
                fixture.setColour(toRed, toGreen, toBlue, self.settings[3].getValue())
            else: 
                fixture.setColour(0, 0, 0, 0)
            self.state = not self.state
            time.sleep(self.settings[4].getValue())