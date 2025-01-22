from Visualiser.Screens.ScreenBase import *
from Visualiser.Components.ButtonComponent import *
from Visualiser.Components.StringInputComponent import *
from Visualiser.Components.HorizontalScrollBarComponent import *
from Resources.Utils import keysWithinDictCheck, fromPercentage

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

        self.register(ButtonComponent("Blackout", (5, 665), (40, 40), blackOutLightsCall))

        def newFixtureScreenCall():
            print("TODO")

        self.register(ButtonComponent("NewFix", (5, 695), (40, 40), newFixtureScreenCall))

        horScroll = self.register(HorScrollBarComponent("FixtureScrollBar", (1, 640), (1278, 18)))
        def updateScrollAmount(com):
            self._scrollXOffset = fromPercentage(0, 1278, com.getScrollAmount())

        horScroll.setScrollUpdateCallback(updateScrollAmount)

    def render(self, vmInstance, pygame, screen, font):
        mousePos = pygame.mouse.get_pos()

        xOffset = -self._scrollXOffset
        fixtureDict = self._controller.getFixtures()
        for fixtureKey in fixtureDict:
            fixture = fixtureDict[fixtureKey]
            fixture.renderFixture(self, pygame, screen, (xOffset, 0), font)
            xOffset += (fixture.getWidth() + self._fixtureSpacing)

        pygame.draw.rect(screen, (75, 75, 75), pygame.Rect(0, 640, 1280, 720))

        for component in self._components:
            component.render(self, pygame, screen, font)
            component.onHover(mousePos)
