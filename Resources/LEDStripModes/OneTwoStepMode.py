from Resources.BlankMode import *
from Settings.Setting import *
from Resources.Utils import msDelay

class OneTwoStepMode(Mode):#TODO complete this.

    cRed = 0
    cGreen = 0
    cBlue = 0

    numSteps = 0
    delay = msDelay()
    displayDelay = msDelay()

    def __init__(self):
        self._name = "OneTwoStep"
        self._fixtureType = "LEDStrip"
        self.settings = [
            Setting("RedFrom", "Sets the Red levels.", 255.0, float),                           # 0
            Setting("GreenFrom", "Sets the Green levels.", 0.0, float),                         # 1
            Setting("BlueFrom", "Sets the Blue levels.", 0.0, float),                           # 2
            Setting("RedTo", "Sets the Red levels.", 0.0, float),                               # 3
            Setting("GreenTo", "Sets the Green levels.", 255.0, float),                         # 4
            Setting("BlueTo", "Sets the Blue levels.", 0.0, float),                             # 5
            Setting("Brightness", "Sets the Brightness levels.", 255, float),                   # 6
            Setting("StepAmount", "Number of steps before pausing.", 4, int),                   # 7
            Setting("StepWaitDuration", "Number of seconds to do a trigger the steps.", 1, int) # 8
        ]

    def onEnable(self, fixture):
        self.delay.reset()
        self.displayDelay.reset()

    def update(self, fixture):##TODO finish this.
        if self.delay.passedMS():
            if self.displayDelay.passedMSReset(1000):
                pass
                #self.cRed = self.getSettings[]
        else:
            pass
            
        fixture.setColour(self.cRed, self.cGreen, self.cBlue, self.settings[6].getValue())