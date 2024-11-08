from Settings.Setting import *
#Just a template Mode.
class Mode():
    _name = None
    controller = None

    settings = []

    def __init__(self):
        self._name = "BLANK"

    def update(self):
        pass

    def getSetting(self, name):
        for x in self.settings:
            if x.getName().lower() == name.lower():
                return x
        return None

    def getName(self):
        return self._name

    def setController(self, controller):
        self.controller = controller