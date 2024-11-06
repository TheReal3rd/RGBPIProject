#import pigpio
from utils import *

#TODO switch to an automated system instead of typing this shit out.
from rgbModes.FadingCycleMode import *

class rgbController():
    #Pinout
    RED_PIN   = 17
    GREEN_PIN = 22
    BLUE_PIN  = 24

    #Colour Modes
    brightness = 255
    r = 255.0
    g = 0.0
    b = 0.0

    #Pin control
    pi = None

    #Colour Mode
    currentMode = None

    modes = None

    #Debug
    testingMode = False

    def __init__(self, testMode):
        self.testingMode = testMode
        if not self.testingMode:
            self.pi = pigpio.pi()

        self.modes = {#NGL i don't like this will change later.
            "FadingCycle" : FadingCycleMode(self),
            "Set" : None
        }

    def update(self):
        if self.currentMode == None:
            self.currentMode = self.modes["FadingCycle"]
        else:
            self.currentMode.update()

        self.sendToPin(self.RED_PIN, self.r)
        self.sendToPin(self.GREEN_PIN, self.g)
        self.sendToPin(self.BLUE_PIN, self.b)

    def sendToPin(self, pin, value):
        realBrightness = int(int(value) * (float(self.brightness) / 255.0))
        if not self.testingMode:
            self.pi.set_PWM_dutycycle(pin, realBrightness)
        else:
            print("{pin} set to {level}".format(pin= pin, level= value))

    def stop(self):
        self.sendToPin(self.RED_PIN, 0)
        self.sendToPin(self.GREEN_PIN, 0)
        self.sendToPin(self.BLUE_PIN, 0)
        self.pi.stop()

    #Setters

    def setColour(self, red, green, blue, brightness):
        self.setRed(red)
        self.setGreen(green)
        self.setBlue(blue)

    def setRed(self, value):
        self.r = clamp(value, 0, 255)

    def setGreen(self, value):
        self.g = clamp(value, 0, 255)

    def setBlue(self, value):
        self.b = clamp(value, 0, 255)

    def setBrightness(self, value):
        self.brightness = clamp(value, 0, 255)

    #Getters