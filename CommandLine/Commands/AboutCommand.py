from CommandBase import *

#Works fine completed.
class AboutCommand(CommandBase):

    def __init__(self):
        super().__init__("About", "Prints out information about this program.")

    def execute(self, args, rgbController, cmdMan):
        print("""
        RGB PI Project
        
        This is a simple Python script used to controle a LED strip for a Raspberry pi.
        This is designed for none addressible LED strips.
        
        Features:
        -Commands System
        -Visuliser for testing
        -Web Panel for control
        """)

    def getHelpMessage(self):
        return self._description
