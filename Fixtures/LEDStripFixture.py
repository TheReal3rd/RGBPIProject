from FixtureBase import *

class LEDStripFixture(FixtureBase):

    _redPin = None
    _greenPin = None
    _bluePin = None

    _currentMode = None

    _red = 0
    _green = 0
    _blue = 0
    _brightness = 255

    def __init__(self, redPin, greenPin, bluePin):
        super().__init__("LEDStrip")

    def update(self):
        pass
