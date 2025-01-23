from Visualiser.Screens.ScreenBase import *
from Visualiser.Components.ButtonComponent import *
from Visualiser.Components.StringInputComponent import *
from Visualiser.Components.HorizontalScrollBarComponent import *
from Visualiser.Components.LabelComponent import *
from Resources.Utils import keysWithinDictCheck, fromPercentage

class NewFixScreen(ScreenBase):

    def __init__(self, vmInstance, controller, dataManager, parent):
        super().__init__("RGB Controller Visualiser", vmInstance, controller, dataManager, parent)

        def goBack():
            self._vmInstance.changeScreen(self._parent)

        self.register(ButtonComponent("Back", (5, 695), (40, 40), goBack))

        self.register(LabelComponent("TEST", (10,10), (40,40)))

    def render(self, vmInstance, pygame, screen, font):
        mousePos = pygame.mouse.get_pos()

        pygame.draw.rect(screen, (75, 75, 75), pygame.Rect(0, 640, 1280, 720))

        for component in self._components:
            component.render(self, pygame, screen, font)
            component.onHover(mousePos)
