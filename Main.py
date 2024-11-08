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
#from _thread import start_new_thread

testMode = True
closing = False

if not testMode:
	import os
	os.system("sudo pigpiod")#Prob wont work cause sudo...

print("RGB Controller started.")
rgbCont = rgbController(testMode)

print("Command Manager started.")
commandLine = CommandManager(rgbCont)
commandLine.start()

if not testMode:
	pass

while closing == False:
	rgbCont.update()

rgbCont.stop()

print("Exitting.")

#start_new_thread(checkKey, ())