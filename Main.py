#Creadits
#Sourced:
#   Original source: https://github.com/dordnung/raspberrypi-ledstrip/tree/master
#   Guide used: https://dordnung.de/raspberrypi-ledstrip/
#Modified:
#	By: TheReal3rd / 3RD
#Personal notes:
#   Pi Pinout: https://learn.sparkfun.com/tutorials/raspberry-gpio/gpio-pinout

from Controller import *
from CommandLine.CommandManager import *
from WebPanel.WebPanelManager import *
from Resources.GlobalDataManager import *
from Settings.Setting import *
import os
import os.path
import json

testMode = True

settings = [
	Setting("OnStartMode", "The mode that starts when the program starts.", "ColourCycle", str),#0
	Setting("UseVisualiser", "Allow the program to create a visualiser window. This is used for test and debugging.", True, bool),#1
	Setting("UseCommand", "Enable or disable the command system.", True, bool),#2
	Setting("UseWebpanel", "Enable or disable the web panel system.", True, bool),#3
	Setting("WebAddress", "Webpanel address this has to be the IP or Domain.", "rgbpi.third.net", str),#4
	Setting("WebPort", "Webpanel port.", 8080, int)#5
]

#Funcs
def saveMain():
	print("Save")
	data = {}
	for x in settings:
		data[x.getName()] = x.getValue()
		
	jsonString = json.dumps(data)
	with open("configs/config.json", "w") as outfile:
		outfile.write(jsonString)


def loadMain():
	print("Load")
	data = {}
	with open("configs/config.json", "r") as jsonFile:
		data = json.load(jsonFile)
    
	for x in settings:
		value = data.get(x.getName())
		
		try:
			valueType = x.getValueType()
			x.setValue(valueType(value))
		except Exception as err:
			x.setValue(x.getDefaultValue())
			print("{SettingName} has been reset".format(SettingName=x.getName()))


#Getter 
def getMainSettings():
	return settings


def close(controller):
	controller.close()
	os._exit(0)

def isTestMode():
	return testMode


if __name__ == "__main__":
	if not testMode:
		os.system("sudo pigpiod")#Prob wont work cause sudo... Seems to work. Yay :3

	#Config Load / Save
	print("Loading the settings.")
	if not os.path.isfile("configs/config.json"):
		saveMain()
	else:
		loadMain()

	print("GlobalData started.")
	dataManager = GlobalDataManager()
		
	print("RGB Controller started.")
	fixController = Controller(dataManager)

	if settings[2].getValue():
		print("Command Manager started.")
		commandLine = CommandManager(fixController)
		commandLine.start()

	if settings[3].getValue():
		print("Webpanel Manager started.")
		webPanel = WebpanelManager(dataManager, fixController, settings[4].getValue(), settings[5].getValue())
		webPanel.start()

	while True:
		fixController.update()