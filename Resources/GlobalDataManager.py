#This is intended to store data that remains the same. For example fixture modes will all be the same for an LED Strip why load a copy for each one?

import glob
import importlib
import inspect
import os
import asyncio
"""#OLD load and save code for mode.
        def save(self):
        for m in self.modes:
            tempMode = self.modes[m]
            if len(tempMode.getSettings()) <= 0:
                continue

            data = {}
            for x in tempMode.getSettings():
                data[x.getName()] = x.getValue()

            jsonString = json.dumps(data)
            with open("ModeSettings/{modeName}Config.json".format(modeName=m), "w") as outfile:
                outfile.write(jsonString)

    def load(self):
        for m in self.modes:
            tempMode = self.modes[m]
            if len(tempMode.getSettings()) <= 0:
                continue

            fileName = "ModeSettings/{modeName}Config.json".format(modeName=m)
            if not os.path.isfile(fileName):
                continue

            data = {}
            with open(fileName) as jsonFile:
                data = json.load(jsonFile)
                    
            for x in tempMode.getSettings():
                value = data.get(x.getName())
                if value == None:
                    x.setValue(x.getDefaultValue())
                else:
                    x.setValue(value)
"""

class GlobalDataManager():#TODO need to re-add mode setting but low priority.

    #LED Strip Data
    stripModes = {}

    #LED Addressible Strip Data


    def __init__(self):
        self.loadLEDStripModes()

    ## Universal funcs

    def getFixureModes(self, fixture):
        match (type(fixture).__name__):
            case "LEDStripFixture":
                return self.getLEDStripModes()
            case _:
                return None


    ## LED Strip specific
    
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
                   
                    self.stripModes[mode.getName().lower()] = mode
                    loadedModesList.append(mode.getName())

        print("LEDStripModes Loaded: {names}".format(names = loadedModesList))

    def getLEDStripModes(self):
        return self.stripModes