from Settings.Setting import *
#Just a template Mode.
class Mode():
    _name = None
    _fixtureType = None
    settings = []

    def __init__(self):
        self._name = "BLANK"
        self._fixtureType = "UnspecifiedType"

    def update(self, fixture):
        pass

    def onEnable(self, fixture):
        pass

    # Getter

    def getSetting(self, name):
        for x in self.settings:
            if x.getName().lower() == name.lower():
                return x
        return None

    def getName(self):
        return self._name

    def getSettings(self):
        return self.settings