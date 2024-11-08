#Template Command
class CommandBase():
    _name = None
    _description = None
    _cont = None

    def __init__(self, name, description, controller):
        self._name = name
        self._description = description
        self._cont = controller

    def execute(self, *args):
        pass

    #Getter

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

