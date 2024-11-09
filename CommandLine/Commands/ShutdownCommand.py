from CommandBase import *
from Main import close

#Works fine completed.
class ShutdownCommand(CommandBase):

    def __init__(self):
        super().__init__("Shutdown", "Shuts this program down. Not the computer its on.")

    def execute(self, args, rgbController, cmdMan):
        print("Shutting down...")
        close(rgbController, cmdMan)

