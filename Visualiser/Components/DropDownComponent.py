from Visualiser.Components.ComponentBase import *

class DropDownComponent(ComponentBase):

    _dropDownValues = None
    _dropDownValueIndex = None

    _DropDownColour = (45, 45, 45)
    _DropDownColourHover = (60, 60, 60)
    _DropDownColourScroller = (90, 90, 90)

    _DropDownOutlineColour = (255, 0, 0)
    _DropDownOutlineColourHover = (0, 255, 0)
    _DropDownColourScrollerHover = (140, 140, 140)

    _labelColour = (255, 255, 255)

    _focus = False

    def __init__(self, name, position, size, valuesArr, valueIndex, includeNone=True):
        super().__init__(name, position, size)

        self._dropDownValues = valuesArr
        self._dropDownValueIndex = valueIndex
        self._focus = False

        if includeNone:
            if not "None" in valuesArr:
                valuesArr.append("None")
            if valueIndex == None or valueIndex == -1:
                self._dropDownValueIndex  = len(valuesArr) - 1

    def render(self, vmInstance, pygame, screen, font):
        colour = self._DropDownColour
        colourOutline = self._DropDownOutlineColour
        scrollerColour = self._DropDownColourScroller

        if self._hover:
            colour = self._DropDownColourHover
            colourOutline = self._DropDownOutlineColourHover
            scrollerColour = self._DropDownColourScrollerHover

        outLineRect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.Rect.inflate_ip(outLineRect, 2,2)
        pygame.draw.rect(screen, colourOutline, outLineRect)

        buttonRect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.draw.rect(screen, colour, buttonRect)

        #Label Draw
        nameLabel = font.render("{name}: ".format(name = self._name), 1, self._labelColour)
        nameWidth, nameHeight = font.size("{name}: ".format(name = self._name))

        lengthOfValuesArr = len(self._dropDownValues)
        if self._dropDownValueIndex >= lengthOfValuesArr:
            self._dropDownValueIndex = 0
        elif self._dropDownValueIndex <= lengthOfValuesArr:
            self._dropDownValueIndex = 0

        valueLabel = font.render("{value}".format(value = self._dropDownValues[self._dropDownValueIndex]), 1, self._labelColour)
        valueWidth, valueHeight = font.size("{value}".format(value = self._dropDownValues[self._dropDownValueIndex]))
        labalSize = (nameWidth + valueWidth, valueHeight)

        self.setSize(labalSize)
        screen.blit(nameLabel, (self._position[0], self._position[1]))
        screen.blit(valueLabel, (self._position[0] + nameWidth, self._position[1]))


    def onClick(self, pos, event):
        self._focus = True

    def onEvent(self, pygame, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self._focus = False

