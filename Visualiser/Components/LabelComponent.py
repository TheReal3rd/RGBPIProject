from Visualiser.Components.ComponentBase import *

class LabelComponent(ComponentBase):#TODO add multiline support.
    _paddingAmount = 5

    _ButtonColour = (45, 45, 45)
    _ButtonColourHover = (60, 60, 60)

    _ButtonOutlineColour = (255, 0, 0)
    _ButtonOutlineColourHover = (0, 255, 0)

    _labelColour = None

    _multiLine = False
    _background = False
    _alignmentState = None

    def __init__(self, name, position, size):
        super().__init__(name, position, size)
        self._labelColour = (255, 255, 255)
        self._alignmentState = 1

    def render(self, vmInstance, pygame, screen, font):
        if self._background:
            colour = self._ButtonColour
            colourOutline = self._ButtonOutlineColour

            if self._hover:
                colour = self._ButtonColourHover
                colourOutline = self._ButtonOutlineColourHover

            outLineRect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
            pygame.Rect.inflate_ip(outLineRect, 6, 6)
            pygame.draw.rect(screen, colourOutline, outLineRect)

            buttonRect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
            pygame.Rect.inflate_ip(buttonRect, 4, 4)
            pygame.draw.rect(screen, colour, buttonRect)

        #Label Draw
        nameLabel = font.render("{name}".format(name = self._name), 1, self._labelColour)
        self.setSize(self.calcSize(self._size, font))
        screen.blit(nameLabel, (self._position[0], self._position[1]))

    def setBackground(self, newState):
        self._background = newState

    def setMultiLine(self, newState):
        self._multiLine = newState

    def setLabelColour(self, newColour):
        self._labelColour = newColour

    def calcSize(self, size, font):
        fsWidth, fsHeight = font.size("{name}".format(name = self._name))
        return (max(size[0], fsWidth), min(size[1], fsHeight))#TODO refine this calc later.

    def setPaddingAmount(self, newPadAmount):
        self._paddingAmount = newPadAmount

    def setAlignment(self, index):
        self._alignmentState = index

    def getAlignmentState(self):
        match(self._alignmentState):
            case 1:
                return "left"
            case 2:
                return "middle"
            case 3:
                return "right"
                 
