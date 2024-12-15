#Sources
#   https://github.com/rpi-ws281x/rpi-ws281x-python/blob/master/examples/strandtest.py

from Fixtures.FixtureBase import *
from Resources.Utils import clamp, rgbInvert
from Main import *

import copy

class LEDStripFixture(FixtureBase):
    _currentMode = None

    _red = 0
    _green = 0
    _blue = 0
    _brightness = 255

    #Pin control
    _pi = None
    _RED_PIN = None
    _GREEN_PIN = None
    _BLUE_PIN = None

    def __init__(self, name, controller, redPin, greenPin, bluePin):
        super().__init__(name, controller)
        if not isTestMode():
            import pigpio
            self.pi = pigpio.pi()
        self._RED_PIN = redPin
        self._GREEN_PIN = greenPin
        self._BLUE_PIN = bluePin
        self.setWidth(128)
        self.setHeight(640)

    def update(self):
        currentMode = self._currentMode
        if currentMode == None:
            self.setCurrentMode(self._controller.getDataManager().getLEDStripModes()["off"])
            return

        self._currentMode.update(self)

    def renderFixture(self, vmInstance, pygame, screen, vec2Pos, font):
        pygame.draw.rect(screen, (self._red, self._green, self._blue), pygame.Rect(vec2Pos[0], vec2Pos[1], self._width, self._height))

        colourInvert = rgbInvert(self._red, self._green, self._blue)
        nameLabel = font.render("{name}".format(name = self._name), 1, (colourInvert[0], colourInvert[1], colourInvert[2]))
        screen.blit(nameLabel, (vec2Pos[0], vec2Pos[1]))

        modeLabel = font.render("{mode}".format(mode = self._currentMode.getName()), 1, (colourInvert[0], colourInvert[1], colourInvert[2]))
        screen.blit(modeLabel, (vec2Pos[0], vec2Pos[1] + 16))

    #Pins

    def sendToPin(self, pin, value):
        realBrightness = int(int(value) * (float(self._brightness) / 255.0))
        if not isTestMode():
            self.pi.set_PWM_dutycycle(pin, realBrightness)

    def updatePins(self):
        self.sendToPin(self._RED_PIN, self._red)
        self.sendToPin(self._GREEN_PIN, self._green)
        self.sendToPin(self._BLUE_PIN, self._blue)

    def stop(self):
        self.sendToPin(self._RED_PIN, 0)
        self.sendToPin(self._GREEN_PIN, 0)
        self.sendToPin(self._BLUE_PIN, 0)

    # Getter

    def getCurrentMode(self):
        self.setColour(0, 0, 0, self._brightness)
        return self._currentMode

    def getColour(self):
        return (self._red, self._green, self._blue)

    def getBrightness(self):
        return self._brightness

    # Setter
    def setCurrentMode(self, mode):
        #if self.visualiser != None:
        #    name = "None"
        #    if mode != None:
        #        name = mode.getName()
        #    self.visualiser.updateMode(name) 
        
        #saveMain()#Saving here causes saves to get corrupted.
        self._currentMode = copy.deepcopy(mode)
        self._currentMode.onEnable(self)

    def setColour(self, red, green, blue, brightness):
        self.setRed(red)
        self.setGreen(green)
        self.setBlue(blue)
        self.setBrightness(brightness)

    def setRed(self, value):
        self._red = clamp(value, 0, 255)

    def setGreen(self, value):
        self._green = clamp(value, 0, 255)

    def setBlue(self, value):
        self._blue = clamp(value, 0, 255)

    def setBrightness(self, value):
        self._brightness = clamp(value, 0, 255)
