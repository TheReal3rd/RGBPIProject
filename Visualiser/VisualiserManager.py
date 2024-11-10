#TKinter
#Sources:
#   https://realpython.com/python-gui-tkinter/
#   https://stackoverflow.com/questions/51591456/can-i-use-rgb-in-tkinter

#TODO Fix the label thingy. But i may switch to using pygame.

from tkinter import *
import _thread
import threading
import time


#Working but incomplete.
class VisualiserManager(threading.Thread):
    _controller = None

    _window = None

    headerText = "RGB Controller Visuliser | Mode: {modeName} | Colour: ({r},{g},{b})"

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = controller

    def run(self):
        self._window = Tk()
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

        canvas = Canvas(window, width = 1280, height = 720, bg="black")
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
