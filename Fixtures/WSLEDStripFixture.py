from Fixtures.FixtureBase import *
from Resources.Utils import clamp
from rpi_ws281x import PixelStrip, Color
from Main import *
import copy
import time

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

    def __init__(self, name, controller, ledPin, ledCount):
        super().__init__(name, controller)
        self._LED_COUNT = ledCount
        self._LED_PIN = ledPin
        if not isTestMode():
            self._strip = PixelStrip(self._LED_COUNT, self._LED_PIN, self._LED_FREQ_HZ, self._LED_DMA, self._LED_INVERT, self._LED_BRIGHTNESS, self._LED_CHANNEL)
            self._strip.begin()

    def update(self):
        if self._currentMode == None:
            self.setCurrentMode(self._controller.getDataManager().getWSLEDStripModes()["off"])
            return

        if not isTestMode():
            self._currentMode.update(self)
        else:
            pass

    # Funcs

    def setPixelColor(self, index, red, green, blue, white):
         self._strip.setPixelColor(index, Color(red, green, blue, white))

    # Getter

    def getStrip(self):
        return self._strip


    def getCurrentMode(self):
        return self._currentMode
        
    # Setter
    def setCurrentMode(self, mode):
        self._currentMode = copy.deepcopy(mode)
        self._currentMode.onEnable(self)
