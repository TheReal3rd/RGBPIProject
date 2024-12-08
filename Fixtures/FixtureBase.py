from abc import ABC, abstractmethod
#Template Fixture. This is intended to add expandability.
class FixtureBase():
    _controller = None
    _name = None
    
    #Render Info
    _width = 64
    _height = 64

    def __init__(self, name, controller):
        self._controller = controller
        self._name = name
        

    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass

    def updatePins(self):
        pass

    def renderFixture(self, vmInstance, pygame, screen, vec2Pos, font):
        if vmInstance.getMissingFixImg() == None:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(vec2Pos[0], vec2Pos[1], self._width, self._height))
            label = font.render("?", 1, (0,0,0))
            screen.blit(label, (vec2Pos[0], vec2Pos[1]))
        else:
            screen.blit(vmInstance.getMissingFixImg(), pygame.Rect(vec2Pos[0], vec2Pos[1], self._width, self._height))
        
    # Getter

    def getName(self):
        return self._name

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    # Setter

    def setWidth(self, width):
        self._width = width

    def setHeight(self, height):
        self._height = height
    