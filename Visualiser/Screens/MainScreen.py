from Visualiser.Screens.ScreenBase import *
from Visualiser.Components.ButtonComponent import *
from Visualiser.Components.StringInputComponent import *
from Visualiser.Components.HorizontalScrollBarComponent import *
from Resources.Utils import keysWithinDictCheck

class MainScreen(ScreenBase):

    #Visuliser
    _fixtureSpacing = 5

    _scrollXOffset = 0

    def __init__(self, controller, dataManager):
        super().__init__("RGB Controller Visualiser", controller, dataManager)

        def blackOutLightsCall():
            fixtures = controller.getFixtures()
            for fixKey in fixtures:
                fixture = fixtures[fixKey]
                modes = dataManager.getFixureModes(fixture)
                if keysWithinDictCheck(["off"], modes):
                    fixture.setCurrentMode(modes["off"])

        self._components.append(ButtonComponent("Blackout", (5, 665), (40, 40), blackOutLightsCall))

        def newFixtureScreenCall():
            print("TODO")

        self._components.append(ButtonComponent("NewFix", (5, 695), (40, 40), newFixtureScreenCall))

        self._components.append(HorScrollBarComponent("FixtureScrollBar", (1, 640), (1278, 18)))


    def render(self, vmInstance, pygame, screen, font):
        mousePos = pygame.mouse.get_pos()

        xOffset = 0
        fixtureDict = self._controller.getFixtures()
        for fixtureKey in fixtureDict:
            fixture = fixtureDict[fixtureKey]
            fixture.renderFixture(self, pygame, screen, (xOffset, 0), font)
            xOffset += fixture.getWidth() + self._fixtureSpacing + self._scrollXOffset

        pygame.draw.rect(screen, (75, 75, 75), pygame.Rect(0, 640, 1280, 720))

        for component in self._components:
            component.render(self, pygame, screen, font)
            component.onHover(mousePos)
