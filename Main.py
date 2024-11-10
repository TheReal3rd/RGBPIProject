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
from Visualiser.VisualiserManager import *
import os

testMode = True


def close(rgbCont):
	rgbCont.stop()
	os._exit(0)

if __name__ == "__main__":
	if not testMode:
		import os
		os.system("sudo pigpiod")#Prob wont work cause sudo...

	print("RGB Controller started.")
	rgbCont = rgbController(testMode)

	print("Command Manager started.")
	commandLine = CommandManager(rgbCont)
	commandLine.start()

	if testMode:
		vm = VisualiserManager(rgbCont)
		vm.start()
		rgbCont.setVisuiliser(vm)

	while True:
		rgbCont.update()