from Visualiser.Screens.ScreenBase import *
from Visualiser.Components.ButtonComponent import *
from Visualiser.Components.StringInputComponent import *
from Visualiser.Components.HorizontalScrollBarComponent import *
from Visualiser.Components.LabelComponent import *
from Visualiser.Components.DropDownComponent import *
from Resources.Utils import keysWithinDictCheck, fromPercentage

class NewFixScreen(ScreenBase):

    def __init__(self, vmInstance, controller, dataManager, parent):
        super().__init__("RGB Controller Visualiser", vmInstance, controller, dataManager, parent)

        def goBack():
            self._vmInstance.changeScreen(self._parent)

        self.register(ButtonComponent("Back", (5, 695), (40, 40), goBack))

        screenSize = vmInstance.getScreenSize()
        title = LabelComponent("New Fixture", ((screenSize[0] / 2), 10), (40,40))
        title.setBackground(False)
        self.register(title)

        self.register(StringInputComponent("FixtureName", ((screenSize[0] / 2), 40), (40,40), ""))

        self.register(DropDownComponent("FixtureType", ((screenSize[0] / 2), 80), (40,40), ["A", "B", "C"], 0))

    def render(self, vmInstance, pygame, screen, font):
        mousePos = pygame.mouse.get_pos()

        pygame.draw.rect(screen, (75, 75, 75), pygame.Rect(0, 640, 1280, 720))

        for component in self._components:
            component.render(self, pygame, screen, font)
            component.onHover(mousePos)
