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
from Visualiser.VisualiserManager import *
from Settings.Setting import *
import os
import os.path
import json


settings = [
	Setting("TestMode", "Puts the software in a test state where it won't send any GPIO commands. For use on a standard computer.", True, bool),#0
	Setting("UseVisualiser", "Allow the program to create a visualiser window. This is used for test and debugging.", True, bool),  			#1
	Setting("UseCommand", "Enable or disable the command system.", True, bool),																	#2
	Setting("UseWebpanel", "Enable or disable the web panel system.", True, bool),																#3
	Setting("WebAddress", "Webpanel address this has to be the IP or Domain.", "rgbpi.third.net", str),											#4
	Setting("WebPort", "Webpanel port.", 8080, int)																								#5
]

testMode = True

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
	#Config Load / Save
	print("Loading the settings.")
	if not os.path.isfile("configs/config.json"):
		saveMain()
	else:
		loadMain()

	testMode = bool(settings[0].getValue())

	if not isTestMode():
		os.system("sudo pigpiod")
		print("Not in a code testing mode.")
	else:
		print("In a code testing mode.")

	print("GlobalData started.")
	dataManager = GlobalDataManager()
		
	print("RGB Controller started.")
	fixController = Controller(dataManager)

	if settings[1].getValue():
		print("Visualiser Manager started.")
		visualiserManager = VisualiserManagerPygame(fixController)
		visualiserManager.start()

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