

class ScreenBase():
    #Screen Data
    _screenTitle = "Fill this in."
    _components = None
    _parent = None

    #Access
    _controller = None
    _dataManager = None
    _vmInstance = None

    def __init__(self, title, vmInstance, controller, dataManager, parent):
        self._screenTitle = title
        self._controller = controller
        self._dataManager = dataManager
        self._parent = parent
        self._vmInstance = vmInstance
        self._components = []

    def render(self, vmInstance, pygame, screen, font):
        pass

    def register(self, newComponent):
        self._components.append(newComponent)
        return newComponent

    #Unfiltered event access. No checks just directly sent.
    def onEvent(self, pygame, event):
        pass

    #Getters

    def getTitle(self):
        return self._screenTitle

    def getComponents(self):
        return self._components

    #Setters