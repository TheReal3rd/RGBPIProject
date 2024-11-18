#Sources:
#   https://pythonbasics.org/webserver/
#   https://stackoverflow.com/questions/21631799/how-can-i-pass-parameters-to-a-requesthandler
#   https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7 #For post request handling.

from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial

import _thread
import threading
import time

class WebServer(BaseHTTPRequestHandler):
    _pagesLoaded = False

    _controller = None

    _indexPage = None 
    _redirectPage = None
    _settingEditPage = None

    _styleSheet = None

    _redirectURL = "/"
    _redirectMessage = "Wasn't filled in. :/"

    def __init__(self, controller, *args, **kwargs):
        self._controller = controller
        super().__init__(*args, **kwargs)
        

    def loadPages(self):
        reader = open("WebPanel/HTML/index.html", "r")
        self._indexPage = reader.read()
        reader = open("WebPanel/HTML/redirect.html", "r")
        self._redirectPage = reader.read()
        reader = open("WebPanel/HTML/settingEdit.html", "r")
        self._settingEditPage = reader.read()
        reader = open("WebPanel/CSS/style.css", "r")
        self._styleSheet = reader.read()

        self._pagesLoaded = True

    def do_GET(self):
        if not self._pagesLoaded:
            self.loadPages()

        params = {}
        cleanPath = self.path
        if self.path.find("?") != -1:
            temp = self.path.split("?")
            cleanPath = temp[0]
            for x in temp[1].split("&"):
                splitOne = x.split("=")
                if len(splitOne) <= 1:
                    continue
                params[splitOne[0]] = splitOne[1]

        if cleanPath in ["/", "/index", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(self.replacements(self._indexPage), "utf-8"))

        elif cleanPath in ["/style"]:
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.end_headers()
            self.wfile.write(bytes(self._styleSheet, "utf-8"))

        elif cleanPath in ["/ModeChange"]:
            #Changes the Mode
            if len(params) != 0:
                newMode = params["modeSelect"]
                if newMode == None:
                    self._redirectMessage = "Mode failed to be changed. Invalid mode provided."
                else:
                    mode = self._controller.getModes()[newMode]
                    self._controller.setCurrentMode(mode)
                    self._redirectMessage = "Mode changed successful."
            else:
                self._redirectMessage = "Mode failed to be changed. No mode provided?"

            #Do reply
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self._redirectURL = "/index"
            self.wfile.write(bytes(self.replacements(self._redirectPage), "utf-8"))

        elif cleanPath in ["/SettingEdit"]:
            failure = False
            failMessage = "Some internal issue."
            setting = None
  
            if len(params) != 0:
                mode = self._controller.getCurrentMode()
                if mode == None:
                    failure = True
                    failMessage = "No mode currently loaded."
                else:
                    if "settingName" in params.keys():
                        setting = mode.getSetting(params["settingName"])
                    else:
                        failure = True
                        failMessage = "Invalid paramter provided."
            else:
                failure = True
                failMessage = "Missing paramaters to use this page."

            #Do reply
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            if failure:
                self._redirectMessage = failMessage
                self._redirectURL = "/index"
                self.wfile.write(bytes(self.replacements(self._redirectPage), "utf-8"))
            else:
                if setting != None:
                    customReplacements = {}
                    customReplacements["[SettingName]"] = setting.getName()
                    customReplacements["[SettingValue]"] = str(setting.getValue())
                    customReplacements["[SettingValueType]"] = str(setting.getValueType().__name__)
                    customReplacements["[SettingDesc]"] = setting.getDescription()


                self.wfile.write(bytes(self.replacements(self._settingEditPage, customReplacements), "utf-8"))

        elif cleanPath in ["/changeSetting"]:
            message = "Internal error."

            if len(params) != 0:
                mode = self._controller.getCurrentMode()
                if mode == None:
                    message = "No mode currently loaded."

                else:
                    if "settingName" in params.keys() and "newValue" in params.keys():
                        setting = mode.getSetting(params["settingName"])
                        try:
                            newValue = params["newValue"]
                            valueType = setting.getValueType()
                            if valueType == bool:
                                if newValue == "True":
                                    setting.setValue(True)
                                else:
                                    setting.setValue(False)

                            else:
                                setting.setValue(valueType(newValue))

                            message = "The value has successfully been changed."
                        except Exception as err:
                            print(err)
                            message = "Provided value throw an exception. Check you entries."
                    else:
                        message = "Invalid paramter provided."
            else:
                message = "Missing paramaters to use this page."
           

            #Do replay
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self._redirectMessage = message
            self._redirectURL = "/index"
            self.wfile.write(bytes(self.replacements(self._redirectPage), "utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self._redirectMessage = "404 Page not found."
            self._redirectURL = "/index.html"
            self.wfile.write(bytes(self.replacements(self._redirectPage), "utf-8"))

    def replacements(self, htmlIn, customReplacements={}):
        controller = self._controller
        if controller == None:
            print("Controller failed to be fetched.")
            return htmlIn

        if htmlIn.find("[CurrentMode]") != -1:
            temp = controller.getCurrentMode()
            result = "None"
            if temp != None:
                result = temp.getName()

            htmlIn = htmlIn.replace("[CurrentMode]", result)

        if htmlIn.find("[RedirectURL]") != -1:
            htmlIn = htmlIn.replace("[RedirectURL]", self._redirectURL)

        if htmlIn.find("[RedirectMessage]") != -1:
            htmlIn = htmlIn.replace("[RedirectMessage]", self._redirectMessage)

        if htmlIn.find("[AvailableModes]") != -1:
            result = ""
            for m in controller.getModes():
                temp = controller.getModes()[m]
                result += '<option value="{simpleMode}">{name}</option>'.format(simpleMode=temp.getName().lower(), name=temp.getName())
            htmlIn = htmlIn.replace("[AvailableModes]", result)
        
        if htmlIn.find("[ModeSettings]") != -1:
            result = ""
            if controller.getCurrentMode() == None:
                result = "None"
            else:
                for s in controller.getCurrentMode().getSettings():
                    result += '<li><a href="/SettingEdit?settingName={SettingSimpleName}"><p>{SettingName}</p></a></li>'.format(SettingSimpleName=s.getName().lower(), SettingName=s.getName())
                    
            htmlIn = htmlIn.replace("[ModeSettings]", result)

        for custom in customReplacements:
            replacement = customReplacements[custom]
            if htmlIn.find(custom) != -1:
                htmlIn = htmlIn.replace(custom, replacement)

        return htmlIn

    #def do_POST(self):#Should idealy use post request to handle changes. But i can't be arsed too. As this panel is intended to be used in a local network. for personal use i feel i don't need to.
    #    contentLength = int(self.headers["Content-Length"])
    #    postData = self.rfile.read(contentLength).decode("utf-8")

class WebpanelManager(threading.Thread):
    _controller = None
    _webserver = None

    _serverAddress = "localhost"
    _serverPort = 8080

    def __init__(self, controller, serverAddress, serverPort, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = controller
        self._serverAddress = serverAddress
        self._serverPort = serverPort

    def run(self):
        hostName = self._serverAddress
        serverPort = self._serverPort

        handler = partial(WebServer, self._controller)

        self._webServer = HTTPServer((hostName, serverPort), handler)
        print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            self._webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        self._webServer.server_close()
        print("Server stopped.")
