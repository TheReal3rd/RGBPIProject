from CommandBase import *

class ModeCommand(CommandBase):

    def __init__(self):
        super().__init__("Mode", "View and Change current RGB mode is running.")

    def execute(self, args, rgbController, cmdMan):
        if len(args) == 3:
            if args[1] in ["c", "change", "s", "set"]:
                newMode = rgbController.getModes()[args[2]]
                if newMode == None:
                    print("Given arguments failed to find a mode under the name of {name} nothing will be done.".format(name=args[2]))
                    return
                rgbController.setCurrentMode(newMode)
                print("Changed RGB Controller mode to {name}.".format(name=newMode.getName()))
        if len(args) == 2:
            if args[1] in ["s","stop"]:
                rgbController.setCurrentMode(None)
        else:
            currentMode = rgbController.getCurrentMode()
            if currentMode == None:
                print("There is no mode running.")
            else:
                print("The RGB Controller is currently running: {name}".format(name=currentMode.getName()))


