import pigpio

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

    def __init__(self):
        self.pi = pigpio.pi()

    def update(self):
        pass

    def sendToPin(self, pin, brightness):
	    realBrightness = int(int(brightness) * (float(self.brightness) / 255.0))
	    self.pi.set_PWM_dutycycle(pin, realBrightness)

    def stop(self)
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