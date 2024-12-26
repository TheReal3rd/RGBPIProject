#TKinter
#Sources:
#   https://realpython.com/python-gui-tkinter/
#   https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter
#   https://realpython.com/pygame-a-primer/

#from Visualiser.Components.ButtonComponent import *
#from Visualiser.Components.StringInputComponent import *
from Visualiser.Screens.MainScreen import *
from Resources.Utils import *
import _thread
import threading
import time

class VisualiserManagerPygame(threading.Thread):
    _controller = None
    _dataManager = None

    _screen = None

    _currentScreen = None

    #Images
    _missingFixImg = None

    def __init__(self, controller, dataManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = controller
        self._dataManager = dataManager
        self._currentScreen = MainScreen(controller, dataManager)

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
            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #mousePos = pygame.mouse.get_pos()
                    if self._currentScreen != None:
                        for component in self._currentScreen.getComponents():
                            if component.isHover():
                                component.onClick(event.pos, event)

                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    if self._currentScreen != None:
                        for component in self._currentScreen.getComponents():
                            if component.isHover():
                                state = event.type == pygame.KEYDOWN
                                component.onKey(event.key, state, event)

                if self._currentScreen != None:
                    self._currentScreen.onEvent(pygame, event)
                    for component in self._currentScreen.getComponents():
                        component.onEvent(pygame, event)
                

            screen.fill((0, 0, 0))

            if self._currentScreen != None:
                self._currentScreen.render(self, pygame, screen, font)

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
