


class ComponentBase():
    _name = None

    _size = None
    _position = None

    _hover = False

    def __init__(self, name, position, size):
        self._name = name
        self._size = size
        self._position = position

    def render(self, vmInstance, pygame, screen, font):
        pass

    #Triggered when the component is clicked when mouse is within its bounds.
    def onClick(self, mousePos, event):
        pass

    #Triggered when key is pressed and the component is hovered over.
    def onKey(self, keyData, down, event):
        pass

    #Unfiltered event access. No checks just directly sent.
    def onEvent(self, pygame, event):
        pass

    #No need to override this as this just changes hover status.
    def onHover(self, mousePos):
        if self.posIntercept(mousePos):
            self._hover = True
        else:
            self._hover = False

    # Funcs

    def posIntercept(self, pos):
        mx = pos[0]
        my = pos[1]

        tx = self._position[0]
        ty = self._position[1]

        bx = self._position[0] + self._size[0]
        by = self._position[1] + self._size[1]

        return mx > tx and my > ty and mx < bx and my < by

    # Getters

    def getName(self):
        return self._name

    def getSize(self):
        return self._size

    def getPosition(self):
        return self._position

    def isHover(self):
        return self._hover

    # Setters

    def setName(self, newName):
        self._name = newName

    def setSize(self, newSize):
        self._size = newSize

    def setPosition(self, newPosition):
        self._position = newPosition