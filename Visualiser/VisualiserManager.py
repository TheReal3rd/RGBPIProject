#TKinter
#Sources:
#   https://realpython.com/python-gui-tkinter/
#   https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter
#   https://realpython.com/pygame-a-primer/

from Visualiser.Components.ButtonComponent import *
from Resources.Utils import *
import _thread
import threading
import time

class VisualiserManagerPygame(threading.Thread):
    _controller = None
    _dataManager = None

    _screen = None

    #Visuliser
    _missingFixImg = None
    _fixtureSpacing = 5

    _components = []

    def __init__(self, controller, dataManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = controller
        self._dataManager = dataManager

        def blackOutLightsCall():
            fixtures = controller.getFixtures()
            for fixKey in fixtures:
                fixture = fixtures[fixKey]
                modes = dataManager.getFixureModes(fixture)
                if keysWithinDictCheck(["off"], modes):
                    fixture.setCurrentMode(modes["off"])
        self._components.append(ButtonComponent("Blackout", (10, 650), (40, 40), blackOutLightsCall))

    def run(self):
        import pygame
        pygame.init()

        clock = pygame.time.Clock()
        fps = 60
        self._missingFixImg = pygame.image.load("Visualiser/Textures/MissingFixture.png")

        self._screen = pygame.display.set_mode([1280, 720])#TODO add screen size checks and possible fallback options such as resize elements and more.
        screen = self._screen
        pygame.display.set_caption("RGB Controller Visualiser")

        font = pygame.font.SysFont("ubuntu", 18, bold=True)

        # render text
        #colourInvert = rgbInvert(colour[0], colour[1], colour[2])
        #label = font.render(self.headerText.format(modeName=self.currentMode, r=colour[0], g=colour[1], b=colour[2], brightness=self._controller.getBrightness()), 1, (colourInvert[0], colourInvert[1], colourInvert[2]))
        #screen.blit(label, (10, 10))

        running = True
        while running:
            mousePos = pygame.mouse.get_pos()

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #mousePos = pygame.mouse.get_pos()
                    for component in self._components:
                        if component.isHover():
                            component.onClick(event.pos)

            screen.fill((0, 0, 0))

            xOffset = 0
            fixtureDict = self._controller.getFixtures()
            for fixtureKey in fixtureDict:
                fixture = fixtureDict[fixtureKey]
                fixture.renderFixture(self, pygame, screen, (xOffset, 0), font)
                xOffset += fixture.getWidth() + self._fixtureSpacing

            pygame.draw.rect(screen, (75, 75, 75), pygame.Rect(0, 640, 1280, 720))

            for component in self._components:
                component.render(self, pygame, screen, font)
                component.onHover(mousePos)

            # Flip the display
            pygame.display.flip()
            pygame.display.update()
            clock.tick(fps)

        # Done! Time to quit.
        pygame.quit()
        from Main import close
        print("Shutting down...")
        close(self._controller)

    def getMissingFixImg(self):
        return self._missingFixImg
