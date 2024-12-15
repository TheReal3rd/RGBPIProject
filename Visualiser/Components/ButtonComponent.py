from Visualiser.Components.ComponentBase import *

class ButtonComponent(ComponentBase):

    _funcCallback = None
    _paddingAmount = 5

    _ButtonColour = (45, 45, 45)
    _ButtonColourHover = (60, 60, 60)

    _ButtonOutlineColour = (255, 0, 0)
    _ButtonOutlineColourHover = (0, 255, 0)

    def __init__(self, name, position, size, funcCallback):
        super().__init__(name, position, size)
        self._funcCallback = funcCallback

    def render(self, vmInstance, pygame, screen, font):
        colour = self._ButtonColour
        colourOutline = self._ButtonOutlineColour

        if self._hover:
            colour = self._ButtonColourHover
            colourOutline = self._ButtonOutlineColourHover

        outLineRect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.Rect.inflate_ip(outLineRect, 6,6)
        pygame.draw.rect(screen, colourOutline, outLineRect)

        buttonRect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.Rect.inflate_ip(buttonRect, 4,4)
        pygame.draw.rect(screen, colour, buttonRect)

        nameLabel = font.render("{name}".format(name = self._name), 1, (255, 255, 255))
        self.setSize(self.calcSize(self._size, font))

        screen.blit(nameLabel, (self._position[0], self._position[1]))

    def onClick(self, pos):
        if not self._funcCallback == None:
            self._funcCallback()

    def calcSize(self, size, font):
        fsWidth, fsHeight = font.size("{name}".format(name = self._name))
        return (max(size[0], fsWidth), min(size[1], fsHeight))#TODO refine this calc later.

    def setPaddingAmount(self, newPadAmount):
        self._paddingAmount = newPadAmount