#This is used to manage all fixtures.
from Fixtures.LEDStripFixture import *
from Fixtures.WSLEDStripFixture import *
from Resources.Utils import keysWithinDictCheck

import glob

class Controller():
    _dataManager = None
    _fixtures = { }

    def __init__(self, dataManager):
        self._dataManager = dataManager
        self.buildFixtures()

    def update(self):
        for fix in self._fixtures.keys():
            fixture = self._fixtures[fix]
            fixture.update()
            fixture.updatePins()

    def buildFixtures(self):
        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

        fixtureAddedList = []

        for file in glob.glob(current_dir + "/configs/fixtures/*.json"):
            data = {}
            with open(file, "r") as jsonFile:
                data = json.load(jsonFile)
            
            if not "Type" in data.keys():
                fName = str(file).replace(current_dir+"/configs/fixtures/", "")
                print("Invalid fixture config at {fileName}".format(fileName=fName))
                continue                

            fixture = data["Type"]
            match(fixture):
                case "LEDStrip":
                    if not keysWithinDictCheck(["Name", "RED_PIN", "GREEN_PIN", "BLUE_PIN"], data):
                        fName = str(file).replace(current_dir+"/configs/fixtures/", "")
                        print("Invalid fixture config at {fileName}. Missing config data required for a LEDStrip. Must have a 'Name' 'RED_PIN' 'GREEN_PIN' 'BLUE_PIN' to operate this fixture.".format(fileName=fName))
                        continue

                    name = data["Name"]
                    redPin = data["RED_PIN"]
                    greenPin = data["GREEN_PIN"]
                    bluePin = data["BLUE_PIN"]

                    finalFixture = LEDStripFixture(name, self, redPin, greenPin, bluePin)
                    self._fixtures[name.lower()] = finalFixture

                    if "CurrentMode" in data.keys():
                        currentMode = self._dataManager.getLEDStripModes()[data["CurrentMode"].lower()]
                        finalFixture.setCurrentMode(currentMode)

                    fixtureAddedList.append("{name}-{type}".format(name=name, type="LEDStrip"))
                case "WSLEDStrip":
                    if not keysWithinDictCheck(["Name", "LED_COUNT", "CTL_PIN"], data):
                        fName = str(file).replace(current_dir+"/configs/fixtures/", "")
                        print("Invalid fixture config at {fileName}. Missing config data required for a WSLEDStrip. Must have a 'Name' 'CTL_PIN' 'LED_COUNT' to operate this fixture.".format(fileName=fName))
                        continue

                    name = data["Name"]
                    ctlPin = data["CTL_PIN"]
                    ledCount = data["LED_COUNT"]

                    finalFixture = WSLEDStripFixture(name, self, ctlPin, ledCount)
                    self._fixtures[name.lower()] = finalFixture

                    # if "CurrentMode" in data.keys():
                    #     currentMode = self._dataManager.getLEDStripModes()[data["CurrentMode"].lower()]
                    #    finalFixture.setCurrentMode(currentMode)

                    fixtureAddedList.append("{name}-{type}".format(name=name, type="WSLEDStrip"))



        print("Loaded Fixtures: {fixList}".format(fixList=fixtureAddedList))
    # Funcs

    def close(self):
        for fix in self._fixtures.keys():
            fixture = self._fixtures[fix]
            fixture.stop()

    def save(self):
        pass

    def load(self):
        pass

    # Getters

    def getFixtures(self):
        return self._fixtures

    def getDataManager(self):
        return self._dataManager

    # Setters