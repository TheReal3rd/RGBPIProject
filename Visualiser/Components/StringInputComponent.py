from Visualiser.Components.ComponentBase import *

class StringInputComponent(ComponentBase):#TODO maybe add a size limitter.
    _value = None
    _valueMaxLength = 20

    _inputMode = False

    _ButtonColour = (45, 45, 45)
    _ButtonColourHover = (60, 60, 60)
    _ButtonColourInputMode = (60, 60, 60)

    _ButtonOutlineColour = (255, 0, 0)
    _ButtonOutlineColourHover = (0, 255, 0)
    _ButtonOutlineColourInputMode = (255, 0, 255)

    def __init__(self, name, position, size, value, maxLength=20):
        super().__init__(name, position, size)
        self._value = value
        self._valueMaxLength = maxLength

    def render(self, vmInstance, pygame, screen, font):
        colour = self._ButtonColour
        colourOutline = self._ButtonOutlineColour

        if self._hover:
            colour = self._ButtonColourHover
            colourOutline = self._ButtonOutlineColourHover

        elif self._inputMode:
            colour = self._ButtonColourInputMode
            colourOutline = self._ButtonOutlineColourInputMode

        outLineRect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.Rect.inflate_ip(outLineRect, 6,6)
        pygame.draw.rect(screen, colourOutline, outLineRect)

        buttonRect = pygame.Rect(self._position[0], self._position[1], self._size[0], self._size[1])
        pygame.Rect.inflate_ip(buttonRect, 4,4)
        pygame.draw.rect(screen, colour, buttonRect)

        label = font.render("{name}: {value}".format(name= self._name, value= self._value), 1, (255, 255, 255))
        screen.blit(label, (self._position[0], self._position[1]))

        self.setSize(self.calcSize(font))

    def onClick(self, mousePos, event):
        self._inputMode = True

    def onEvent(self, pygame, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            if not self.posIntercept(mousePos):
                self._inputMode = False

        elif self._inputMode and (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
            state = event.type == pygame.KEYDOWN
            if state:
                if event.key == pygame.K_BACKSPACE:
                    self._value = self._value[:-1]
                else:
                    if len(self._value) < self._valueMaxLength:
                        self._value += event.unicode

    def calcSize(self, font):
        dummyValue = "".ljust(self._valueMaxLength, "a")
        return font.size("{name}: {value}".format(name= self._name, value= dummyValue))

    #Setters

    def setValue(self, value):
        self._value = value

    #Getters

    def getValue(self):
        return self._value