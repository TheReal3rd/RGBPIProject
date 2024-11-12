#Creadits
#Sourced:
#   Original source: https://github.com/dordnung/raspberrypi-ledstrip/tree/master
#   Guide used: https://dordnung.de/raspberrypi-ledstrip/
#Modified:
#	By: TheReal3rd / 3RD
#Personal notes:
#   Pi Pinout: https://learn.sparkfun.com/tutorials/raspberry-gpio/gpio-pinout

from rgbController import *
from CommandLine.CommandManager import *
from Settings.Setting import *
import os
import json

testMode = True

settings = [
	Setting("OnStartMode", "The mode that starts when the program starts.", "ColourCycle", str)
]

def save():
    data = {}
    for x in settings:
        data[x.getName()] = x.getValue()

    jsonString = json.dumps(data)
    with open("config.json", "w") as outfile:
        outfile.write(jsonString)

def load():
    data = {}
    with open("config.json") as jsonFile:
        data = json.load(jsonFile)
            
    for x in settings:
        value = data.get(x.getName())
        if value == None:
            x.setValue(x.getDefaultValue())
        else:
            x.setValue(value)


def close(rgbCont):
	rgbCont.stop()
	os._exit(0)

if __name__ == "__main__":
	if not testMode:
		import os
		os.system("sudo pigpiod")#Prob wont work cause sudo...

	#Config Load / Save
	print("Loading the settings.")
	load()
	save()

	print("RGB Controller started.")
	rgbCont = rgbController(testMode, settings[0].getValue())
	rgbCont.load()
	rgbCont.save()

	print("Command Manager started.")
	commandLine = CommandManager(rgbCont)
	commandLine.start()

	if testMode:
		from Visualiser.VisualiserManager import * #This fixes issues related to having no GUI on the PI
		vm = VisualiserManager(rgbCont)
		vm.start()
		rgbCont.setVisuiliser(vm)

	while True:
		rgbCont.update()