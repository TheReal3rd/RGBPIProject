from CommandBase import *
from Utils import fetchDeviceTemps

#Works fine completed.
class TemperatureCommand(CommandBase):

    def __init__(self):
        super().__init__("Temps", "Displays the devices current tempreture.")

    def execute(self, args, rgbController, cmdMan):
        result = fetchDeviceTemps()
        if result == "-1":
            print("This device isn't a raspberry pi... It's not supported for this.")
        else:
            print("The device temperature: {temps}".format(temps=result))

