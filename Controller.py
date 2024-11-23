#This is used to manage all fixtures.
from Fixtures.LEDStripFixture import *

class Controller():
    _dataManager = None
    _fixtures = { }

    def __init__(self, dataManager):
        self._dataManager = dataManager
        self.buildFixtures()

        #For testing
        self._fixtures["TestStrip"] = LEDStripFixture(self, 17, 22, 24)

    def update(self):
        for fix in self._fixtures.keys():
            fixture = self._fixtures[fix]
            fixture.update()
            fixture.updatePins()

    def buildFixtures(self):
        pass

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