from Fixtures.FixtureBase import *
from Resources.Utils import clamp
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

    def __init__(self, name, controller, ledPin, ledCount):
        super().__init__(name, controller)
        self._LED_COUNT = ledCount
        self._LED_PIN = ledPin
        if not isTestMode():
            from rpi_ws281x import PixelStrip, Color
            self._strip = PixelStrip(self._LED_COUNT, self._LED_PIN, self._LED_FREQ_HZ, self._LED_DMA, self._LED_INVERT, self._LED_BRIGHTNESS, self._LED_CHANNEL)
            self._strip.begin()

    def update(self):
        if not isTestMode():
            for j in range(256 * iterations):
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, wheel((i + j) & 255))
                strip.show()
                time.sleep(wait_ms / 1000.0)