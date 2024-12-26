from Visualiser.Components.ComponentBase import *

class HorScrollBarComponent(ComponentBase):

    _paddingAmount = 5

    _ButtonColour = (45, 45, 45)
    _ButtonColourHover = (60, 60, 60)

    _ButtonOutlineColour = (255, 0, 0)
    _ButtonOutlineColourHover = (0, 255, 0)

    _scrollAmount = 0

    def __init__(self, name, position, size):
        super().__init__(name, position, size)

    def render(self, vmInstance, pygame, screen, font):
        colour = self._ButtonColour
        colourOutline = self._ButtonOutlineColour

        if self._hover:
            colour = self._ButtonColourHover
            colourOutline = self._ButtonOutlineColourHover

        outLineRect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.Rect.inflate_ip(outLineRect, 2,2)
        pygame.draw.rect(screen, colourOutline, outLineRect)

        buttonRect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.draw.rect(screen, colour, buttonRect)

    def onClick(self, pos, event):
        pass

    def calcSize(self, size, font):
        fsWidth, fsHeight = font.size("{name}".format(name = self._name))
        return (max(size[0], fsWidth), min(size[1], fsHeight))#TODO refine this calc later.

    # Setters

    def setPaddingAmount(self, newPadAmount):
        self._paddingAmount = newPadAmount

    # Getters