from abc import ABC, abstractmethod
#Template Fixture. This is intended to add expandability.
class FixtureBase():
    _controller = None
    _name = None
    
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

    # Getter

    def getName(self):
        return self._name

    # Setter
    