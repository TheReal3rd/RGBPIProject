#Template Command
class CommandBase():
    _name = None
    _description = None

    def __init__(self, name, description):
        self._name = name
        self._description = description

    def execute(self, args, rgbController, cmdMan):
        pass

    #Getter

    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def getHelpMessage(self):
        return "There is no help message for this command yet."

    #Setter

