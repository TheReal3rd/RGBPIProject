from Fixtures.FixtureBase import *
from Resources.Utils import clamp
from Main import *
import copy
import time

if not isTestMode():
    from rpi_ws281x import PixelStrip, Color

#TODO known issue the program breaks when on raspberry pi. Without the import being here. Try finding a fix that works consistantly.

class WSLEDStripFixture(FixtureBase):

    #Adjust these
    _LED_COUNT = 16        # Number of LED pixels.
    _LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
    _LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest

    #Prolly don't need to adjust these values.
    _LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    _LED_DMA = 10          # DMA channel to use for generating signal (try 10)
    _LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
    _LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    _strip = None
    _currentMode = None

    #Visualiser
    _pixels = None
    _pixelHeight = 0
    _pixelAmount = 40

    def __init__(self, name, controller, ledPin, ledCount):
        super().__init__(name, controller)
        self._LED_COUNT = ledCount
        self._LED_PIN = ledPin
        self.setWidth(128)
        self.setHeight(640)
        self._pixels = [ledCount]
        if not isTestMode():
            from rpi_ws281x import PixelStrip, Color
            self._strip = PixelStrip(self._LED_COUNT, self._LED_PIN, self._LED_FREQ_HZ, self._LED_DMA, self._LED_INVERT, self._LED_BRIGHTNESS, self._LED_CHANNEL)
            self._strip.begin()
        else:
            for x in range(0, self._pixelAmount):
                self._pixels.append( (255, 255, 255) )
            self._pixelHeight = self.calcPixelHeight()

    def update(self):
        if self._currentMode == None:
            self.setCurrentMode(self._controller.getDataManager().getWSLEDStripModes()["off"])
            return

        self._currentMode.update(self)

    
    def renderFixture(self, vmInstance, pygame, screen, vec2Pos, font):
        yOffset = 0
        for pixel in self._pixels:
            pygame.draw.rect(screen, pixel, pygame.Rect(vec2Pos[0], vec2Pos[1] + yOffset, self._width, self._pixelHeight))
            yOffset = yOffset + self._pixelHeight + 2

        colour = self._pixels[0]
        textColour = rgbInvert(colour[0], colour[1], colour[2])
        nameLabel = font.render("{name}".format(name = self._name), 1, textColour)
        screen.blit(nameLabel, (vec2Pos[0], vec2Pos[1]))

        modeLabel = font.render("{mode}".format(mode = self._currentMode.getName()), 1, textColour)
        screen.blit(modeLabel, (vec2Pos[0], vec2Pos[1] + 16))


    def stop(self):
        if not isTestMode():
            self.wipeColour()

    # Funcs

    def calcPixelHeight(self):
        height1 = self.getHeight() / self.getNumPixels()

        while ((height1 + 2) * self.getNumPixels()) > self.getHeight():
            height1 -= 0.5

        return height1

    def setPixelColour(self, index, red, green, blue, white):
        if not isTestMode():
            self._strip.setPixelColor(index, Color(red, green, blue, white))
        else:
            self._pixels[index] = (red, green, blue)

    def getNumPixels(self):
        if not isTestMode():
            return self._strip.numPixels()
        else:
            return len(self._pixels)

    def show(self):
        if not isTestMode():
            self._strip.show()

    def setBrightness(self, value):
        if not isTestMode():
            self._strip.setBrightness(value)

    def wipeColour(self, delay=None):
        for x in range(self.getNumPixels()):
            self.setPixelColour(x, 0, 0, 0, 0)
            if delay != None:
                self.show()
                time.sleep(delay)

        if delay == None:
            self.show()
         
    # Getter

    def getStrip(self):
        return self._strip

    def getCurrentMode(self):
        return self._currentMode
        
    # Setter

    def setCurrentMode(self, mode):
        self._currentMode = copy.deepcopy(mode)
        self._currentMode.onEnable(self)
