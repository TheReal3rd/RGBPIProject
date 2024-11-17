#TKinter
#Sources:
#   https://realpython.com/python-gui-tkinter/
#   https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter
#   https://realpython.com/pygame-a-primer/

#TODO Add a TKinter and pygame vis allow the user to select and fallbacks.
from Utils import *
import _thread
import threading
import time

class VisualiserManagerPygame(threading.Thread):
    _controller = None

    _screen = None

    headerText = "Mode: {modeName} | Col: ({r},{g},{b}) | Bri: {brightness}"
    currentMode = "None"

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = controller
        self.currentMode = self._controller.getCurrentMode().getName()

    def updateMode(self, modeName):
        self.currentMode = modeName

    def run(self):
        import pygame
        pygame.init()

        clock = pygame.time.Clock()
        fps = 60

        self._screen = pygame.display.set_mode([1280, 720])
        screen = self._screen
        pygame.display.set_caption("RGB Controller Visualiser")

        font = pygame.font.SysFont("ubuntu", 18, bold=True)

        running = True
        while running:

            # Did the user click the window close button?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False


            colour = self._controller.getColour()
            screen.fill((colour[0], colour[1], colour[2]))

            # render text
            colourInvert = rgbInvert(colour[0], colour[1], colour[2])
            label = font.render(self.headerText.format(modeName=self.currentMode, r=colour[0], g=colour[1], b=colour[2], brightness=self._controller.getBrightness()), 1, (colourInvert[0], colourInvert[1], colourInvert[2]))
            screen.blit(label, (10, 10))


            # Flip the display
            pygame.display.flip()
            pygame.display.update()
            clock.tick(fps)

        # Done! Time to quit.
        pygame.quit()
        from Main import close
        print("Shutting down...")
        close(self._controller)


#Working but ~~incomplete~~. Will not complete i am planning to use Pygame cause CBA to fix issues related to TKinter
class VisualiserManagerTK(threading.Thread):
    _controller = None

    _window = None

    #headerText = "RGB Controller Visualiser | Mode: {modeName} | Colour: ({r},{g},{b})"

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = controller


    def updateMode(self, modeName):
        pass

    def run(self):
        import tkinter as tk
        self._window = tk.Tk()
        window = self._window

        #Setup window sizing.
        window.geometry("1280x720")
        window.resizable(False, False)
        #Stylisation
        window.configure(background='black')
        window.title("RGB Controller Visualiser")
        #Changing a labels text breaks everything. IDK why it reset the RGB back to 0 for seemingly no reason. Maybe a thread realted issue but idk... I fucking hate Python.
        #header = Label(text=self.headerText.format(modeName=self.getModeName(), r=0,g=0,b=0), fg="white", bg="black")
        #header.pack()

        def onClose():
            from Main import close
            print("Shutting down...")
            close(self._controller)

        window.protocol("WM_DELETE_WINDOW", onClose)

        canvas = tk.Canvas(window, width = 1280, height = 720, bg="black")
        canvas.pack()

        while True:
            colour = self._controller.getColour()
            canvas.configure(bg=self._from_rgb(colour))
            #header.config(text=self.headerText.format(modeName=self.getModeName(), r=self.red, g=self.green, b=self.blue))
            window.update()
            #time.sleep(0.3)


    def _from_rgb(self, rgb):
        rgb = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
        return "#%02x%02x%02x" % rgb   

    def getModeName(self):
        result = "None"
        currentMode = self._controller.getCurrentMode()
        if not currentMode == None:
            result = currentMode.getName()
        return result
