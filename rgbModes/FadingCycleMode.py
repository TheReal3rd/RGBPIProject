from rgbModes.BlankMode import *

#Works fine.
#Cylces through the colour using a fading effect.
class FadingCycleMode(Mode):
    stage = 0
    reverse = False

    r = 0
    g = 0
    b = 0

    def __init__(self, controller):
        self.name = "Fading"
        self.controller = controller

    def update(self):
        if self.stage == 0:
            self.controller.setRed(self.r)
            if self.reverse:
                self.r -= 1

                if self.r <= 0:
                    self.stage = 1

            else:
                self.r += 1

                if self.r >= 255:
                    self.stage = 1

        elif self.stage == 1:
            self.controller.setGreen(self.g)
            if self.reverse:
                self.g -= 1

                if self.g <= 0:
                    self.stage = 2

            else:
                self.g += 1

                if self.g >= 255:
                    self.stage = 2

        elif self.stage == 2:
            self.controller.setBlue(self.b)

            if self.reverse:
                self.b -= 1

                if self.b <= 0:
                    self.stage = 0
                    self.reverse = False

            else:
                self.b += 1

                if self.b >= 255:
                    self.stage = 0
                    self.reverse = True