#This is intended to store data that remains the same. For example fixture modes will all be the same for an LED Strip why load a copy for each one?

import glob
import importlib
import inspect
import os
import asyncio


class GlobalDataManager():

    #LED Strip Data
    stripModes = {}

    #LED Addressible Strip Data


    def __init__(self):
        self.loadLEDStripModes()


    def loadLEDStripModes(self):
        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        current_module_name = os.path.splitext(os.path.basename(current_dir))[0]

        loadedModesList = []

        for file in glob.glob(current_dir + "/LEDStripModes/*.py"):
            name = os.path.splitext(os.path.basename(file))[0]
            
            # Ignore __ files
            if name.startswith("__"):
                continue

            module = importlib.import_module("." + name, package="Resources.LEDStripModes")#package=current_module_name

            for member in dir(module):
                if not member.endswith("Mode"):
                    continue

                handlerClass = getattr(module, member)

                if handlerClass and inspect.isclass(handlerClass) and not handlerClass.__name__ == "BlankMode":
                    mode = handlerClass()
                    if mode.getName() == "BLANK":
                        continue
                    #mode.setController(self)
                    self.stripModes[mode.getName().lower()] = mode
                    loadedModesList.append(mode.getName())

        print("LEDStripModes Loaded: {names}".format(names = loadedModesList))