#import pigpio
from Utils import *
from Settings.Setting import *

import time

import glob
import importlib
import inspect
import os
import asyncio
import json

class rgbController():
    #Pinout
    RED_PIN   = 17
    GREEN_PIN = 22
    BLUE_PIN  = 24

    #Colour Modes
    brightness = 255.0
    r = 0.0
    g = 0.0
    b = 0.0

    #Pin control
    pi = None

    #Colour Mode
    currentMode = None

    modes = {}

    #Debug
    testingMode = False
    visualiser = None

    def __init__(self, testMode, startWith):
        self.testingMode = testMode
        if not self.testingMode:
            import pigpio
            self.pi = pigpio.pi()
        self.loadModes()

        self.load()
        self.save()

        if not (startWith == None or startWith == ""):
            self.currentMode = self.modes[startWith.lower()]

    def update(self):
        if self.testingMode:
            time.sleep(0.02)

        #print(str(self.r) + " | " + str(self.g) + " | " + str(self.b))
        if self.currentMode == None:
            self.r = 0
            self.g = 0
            self.b = 0
        else:
            self.currentMode.update()

        self.sendToPin(self.RED_PIN, self.r)
        self.sendToPin(self.GREEN_PIN, self.g)
        self.sendToPin(self.BLUE_PIN, self.b)

    def sendToPin(self, pin, value):
        realBrightness = int(int(value) * (float(self.brightness) / 255.0))
        if not self.testingMode:
            self.pi.set_PWM_dutycycle(pin, realBrightness)

    def stop(self):
        self.sendToPin(self.RED_PIN, 0)
        self.sendToPin(self.GREEN_PIN, 0)
        self.sendToPin(self.BLUE_PIN, 0)
        #self.pi.close()

    def save(self):
        for m in self.modes:
            tempMode = self.modes[m]

            data = {}
            for x in tempMode.getSettings():
                data[x.getName()] = x.getValue()

            jsonString = json.dumps(data)
            with open("ModeSettings/{modeName}Config.json".format(modeName=m), "w") as outfile:
                outfile.write(jsonString)

    def load(self):
        for m in self.modes:
            tempMode = self.modes[m]

            data = {}
            with open("ModeSettings/{modeName}Config.json".format(modeName=m)) as jsonFile:
                data = json.load(jsonFile)
                    
            for x in tempMode.getSettings():
                value = data.get(x.getName())
                x.setValue(value)


    #Loads command into the commands list. Copied from the AilisBot Project. (Very hacked together... Lol i had alot of issue with this but it now works. :3)
    #Src: https://stackoverflow.com/questions/3178285/list-classes-in-directory-python
    def loadModes(self):
        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        current_module_name = os.path.splitext(os.path.basename(current_dir))[0]
        for file in glob.glob(current_dir + "/rgbModes/*.py"):
            name = os.path.splitext(os.path.basename(file))[0]

            # Ignore __ files
            if name.startswith("__"):
                continue
            module = importlib.import_module("." + name, package="rgbModes")#package=current_module_name

            for member in dir(module):
                if not member.endswith("Mode"):
                    continue

                handlerClass = getattr(module, member)

                if handlerClass and inspect.isclass(handlerClass) and not handlerClass.__name__ == "BlankMode":
                    mode = handlerClass()
                    if mode.getName() == "BLANK":
                        continue
                    mode.setController(self)
                    self.modes[mode.getName().lower()] = mode
                    print("Loaded RGBController Mode: {name}".format(name = mode.getName()))

    #Setters

    def setColour(self, red, green, blue, brightness):
        self.setRed(red)
        self.setGreen(green)
        self.setBlue(blue)
        self.setBrightness(brightness)

    def setRed(self, value):
        self.r = clamp(value, 0, 255)

    def setGreen(self, value):
        self.g = clamp(value, 0, 255)

    def setBlue(self, value):
        self.b = clamp(value, 0, 255)

    def setBrightness(self, value):
        self.brightness = clamp(value, 0, 255)

    def setCurrentMode(self, mode):
        self.currentMode = mode

    def setVisuiliser(self, vis):
        self.visualiser = vis

    #Getters

    def getCurrentMode(self):
        self.setColour(0, 0, 0, self.brightness)
        return self.currentMode

    def getModes(self):
        return self.modes

    def getColour(self):
        return (self.r, self.g, self.b)

    def getBrightness(self):
        return self.brightness