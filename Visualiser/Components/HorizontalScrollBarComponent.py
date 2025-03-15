from Visualiser.Components.ComponentBase import *
from Resources.Utils import *

class HorScrollBarComponent(ComponentBase):

    #_paddingAmount = 5

    _ButtonColour = (45, 45, 45)
    _ButtonColourHover = (60, 60, 60)
    _ButtonColourScroller = (90, 90, 90)

    _ButtonOutlineColour = (255, 0, 0)
    _ButtonOutlineColourHover = (0, 255, 0)
    _ButtonColourScrollerHover = (140, 140, 140)

    _scrollerWidth = 40
    _scrollAmount = 0
    _scrollerHeld = False

    _scrollUpdateCallBack = None

    def __init__(self, name, position, size):
        super().__init__(name, position, size)

    def render(self, vmInstance, pygame, screen, font):
        colour = self._ButtonColour
        colourOutline = self._ButtonOutlineColour
        scrollerColour = self._ButtonColourScroller

        if self._hover:
            colour = self._ButtonColourHover
            colourOutline = self._ButtonOutlineColourHover
            scrollerColour = self._ButtonColourScrollerHover

        outLineRect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.Rect.inflate_ip(outLineRect, 2,2)
        pygame.draw.rect(screen, colourOutline, outLineRect)

        buttonRect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.draw.rect(screen, colour, buttonRect)

        scrollerPos = fromPercentage(2.0, float((self._size[0] - self._scrollerWidth) + 2), self._scrollAmount)
        scrollerPos = clamp(scrollerPos, 1.0, float((self._size[0] - self._scrollerWidth) + 2))#Not sure why the percentage isn't accurate probably cause im reusing Java code.

        scrollerRect = pygame.Rect(scrollerPos, self._position[1], self._scrollerWidth, self._size[1])
        pygame.draw.rect(screen, scrollerColour, scrollerRect)

        if self._scrollerHeld:
            if self._scrollUpdateCallBack != None:
                self._scrollUpdateCallBack(self)

            mousePos = pygame.mouse.get_pos()
            newScrollPos = toPercentage(2.0, float((self._size[0] - self._scrollerWidth) + 2), mousePos[0] - (self._scrollerWidth / 2))
            newScrollPos = clamp(newScrollPos, 0.0, float((self._size[0] - self._scrollerWidth) + 2))
            self._scrollAmount = newScrollPos

    def onClick(self, pos, event):
        self._scrollerHeld = True

    def onEvent(self, pygame, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self._scrollerHeld = False

    def calcSize(self, size, font):
        fsWidth, fsHeight = font.size("{name}".format(name = self._name))
        return (max(size[0], fsWidth), min(size[1], fsHeight))#TODO refine this calc later.

    # Setters

    #def setPaddingAmount(self, newPadAmount):
    #    self._paddingAmount = newPadAmount

    def setScrollUpdateCallback(self, newCallback):
        self._scrollUpdateCallBack = newCallback

    def setScrollerWidth(self, newScrollerWidth):
        self._scrollerWidth = newScrollerWidth

    # Getters

    def getScrollAmount(self):
        return self._scrollAmount