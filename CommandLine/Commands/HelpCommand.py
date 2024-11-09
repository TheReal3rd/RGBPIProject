from CommandBase import *


#Works fine completed.
class HelpCommand(CommandBase):

    def __init__(self):
        super().__init__("Help", "Prints out help information for a commands.")

    def execute(self, args, rgbController, cmdMan):
        if len(args) >= 2:
            command = cmdMan.getCommands()[args[1]]
            if command == None:
                print("Request help message for command {request} doesn't exist... Check your spelling.".format(request = args[1]))
            else:
                print(command.getHelpMessage())
        else:
            for cmd in cmdMan.getCommands():
                command = cmdMan.getCommands()[cmd]
                print("Command: {name} - {desc}".format(name = command.getName(), desc = command.getDescription()))

