import _thread
import threading

import glob
import importlib
import inspect
import os
import asyncio


class CommandManager(threading.Thread):
    stopping = False

    rgbCont = None

    commandDict = {}

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgbCont = controller
        self.loadCommands()
     
    def run(self):
        while not self.stopping:
            request = input("Command: ")
            args = request.split(" ")
            command = self.commandDict[args[0].lower()]
            if command == None:
                print("Command {name} doesn't exist. Check your spelling or use help.".format(name=args[0]))
            else:
                print("Executing... {commandReq}".format(commandReq=request))
                command.execute(args, self.rgbCont, self)

    def loadCommands(self):
        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        current_module_name = os.path.splitext(os.path.basename(current_dir))[0]
        for file in glob.glob(current_dir + "/Commands/*.py"):
            name = os.path.splitext(os.path.basename(file))[0]

            # Ignore __ files
            if name.startswith("__"):
                continue
            module = importlib.import_module(".Commands." + name,package=current_module_name)

            for member in dir(module):
                handlerClass = getattr(module, member) 

                if handlerClass and inspect.isclass(handlerClass) and not handlerClass.__name__ == "CommandBase":
                    command = handlerClass()
                    self.commandDict[command.getName().lower()] = command
                    print("Loaded CommandManager Command: {name}".format(name = command.getName()))

    #Getter

    def getCommands(self):
        return self.commandDict