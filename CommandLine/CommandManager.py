import _thread
import threading


class CommandManager(threading.Thread):
    stopping = False

    rgbCont = None

    commandDict = {
        
    }

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rgbCont = controller
     
    def run(self):
        while not self.stopping:
            request = input("Command: ")

            

            print("Executing... {commandReq}".format(commandReq=request))