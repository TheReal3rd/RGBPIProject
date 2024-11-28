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

class GlobalDataManager():#TODO need to re-add mode settings saving but low priority.

    #LED Strip Data
    _stripModes = {}

    #WS LED Addressible Strip Data
    _wsStripModes = {}


    def __init__(self):
        self._stripModes = self.loadModes("LEDStripModes")
        self._wsStripModes = self.loadModes("WSLEDStripModes")

    ## Universal funcs

    def getFixureModes(self, fixture):
        match (type(fixture).__name__):
            case "LEDStripFixture":
                return self.getLEDStripModes()
            case "WSLEDStripFixture":
                return self.getWSLEDStripModes()
            case _:
                return None
    
    def loadModes(self, folderName):
        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        current_module_name = os.path.splitext(os.path.basename(current_dir))[0]
        resultDict = {}

        for file in glob.glob("{currentDir}/{folderName}/*.py".format(currentDir=current_dir, folderName=folderName)):
            name = os.path.splitext(os.path.basename(file))[0]

            # Ignore __ files
            if name.startswith("__"):
                continue

            module = importlib.import_module("." + name, package="Resources.{folderName}".format(folderName=folderName))

            for member in dir(module):
                if not member.endswith("Mode"):
                    continue

                handlerClass = getattr(module, member)

                if handlerClass and inspect.isclass(handlerClass):
                    mode = handlerClass()
                    resultDict[mode.getName().lower()] = mode

    
    def getLEDStripModes(self):
        return self._stripModes

    def getWSLEDStripModes(self):
        return self._wsStripModes