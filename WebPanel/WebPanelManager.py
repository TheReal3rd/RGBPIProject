#Sources:
#   https://pythonbasics.org/webserver/
#   https://stackoverflow.com/questions/21631799/how-can-i-pass-parameters-to-a-requesthandler
#   https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7 #For post request handling.
#   https://search.brave.com/search?q=html+scale+everything+bigger+when+on+phone&source=web&summary=1&summary_og=5217f18885f2abcceb2171
#   https://stackoverflow.com/questions/9205081/is-there-a-way-to-store-a-function-in-a-list-or-dictionary-so-that-when-the-inde

#   https://www.geeksforgeeks.org/python-match-case-statement/ I didn't know Python a a switch statement equivelent! yay.
#   https://www.tutorialspoint.com/python/python_matchcase_statement.htm

from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial
from Resources.Utils import fetchDeviceTemps

import _thread
import threading
import time


class WebServer(BaseHTTPRequestHandler):
    _pagesLoaded = False

    _controller = None
    _dataManager = None

    _indexPage = None 
    _redirectPage = None
    _viewFixturePage = None

    _styleSheet = None

    _redirectURL = "/"
    _redirectMessage = "Wasn't filled in. :/"

    _replacementDict = {}

    def __init__(self, dataManager, controller, *args, **kwargs):
        self._dataManager = dataManager
        self._controller = controller
        self._replacementDict = {
            "[RedirectURL]" : self.getRedirectURL,
            "[RedirectMessage]" : self.getRedirectMessage,
            "[CurrentTemp]" : fetchDeviceTemps,
            "[FixtureList]" : self.getFixtureList,
            "[NumFixtures]" : self.getFixtureCount
        }
        super().__init__(*args, **kwargs)

    def loadPages(self):
        reader = open("WebPanel/HTML/index.html", "r")
        self._indexPage = reader.read()

        reader = open("WebPanel/HTML/redirect.html", "r")
        self._redirectPage = reader.read()

        reader = open("WebPanel/HTML/viewFixture.html", "r")
        self._viewFixturePage = reader.read()

        reader = open("WebPanel/CSS/style.css", "r")
        self._styleSheet = reader.read()

        self._pagesLoaded = True

    
    def do_GET(self):
        if not self._pagesLoaded:
            self.loadPages()
        #Param handler
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

        #Page Responses.
        match (cleanPath):
            case "/" | "/index" |  "/index.html":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes(self.replacements(self._indexPage), "utf-8"))
            case "/style":
                self.send_response(200)
                self.send_header("Content-type", "text/css")
                self.end_headers()
                self.wfile.write(bytes(self._styleSheet, "utf-8"))
            case "/ViewFixture":
                failure = False
                failMessage = "This error message wasn't filled in..."
                customReplacements = {}
                if "fixture" in params.keys():
                    fixName = params["fixture"]
                    fixtures = self._controller.getFixtures()
                    if fixName in fixtures.keys():
                        fixture = fixtures[fixName]

                        customReplacements["[FixtureName]"] = fixture.getName()
                        customReplacements["[FixtureNameLower]"] = fixture.getName().lower()
                        customReplacements["[FixtureType]"] = type(fixture).__name__

                        modeName = "None"
                        currentMode = fixture.getCurrentMode()
                        if not currentMode == None:
                            modeName = currentMode.getName()

                            #Fixture Mode Settings
                            fixtureModeSettingsResult = "<p>This Mode doesn't have any settings associated to it.</p>"
                            fixtureModeSettings = currentMode.getSettings()
                            if len(fixtureModeSettings) >= 1:
                                fixtureModeSettingsResult = ""
                                for set in fixtureModeSettings:
                                    fixtureModeSettingsResult += '<li><a href="/FixtureSettingEdit?FixtureName={FixtureName}&settingName={SettingSimpleName}"><p> Edit -> {SettingName}</p></a></li>'.format(FixtureName=fixture.getName().lower(), SettingSimpleName=set.getName().lower(), SettingName=set.getName())

                        customReplacements["[FixtureMode]"] = modeName 
                        customReplacements["[FixtureModeSettings]"] = fixtureModeSettingsResult

                        fixtureModes = self._dataManager.getFixureModes(fixture)
                        fixtureModeResult = "<p>This fixture doesn't have any modes associated to it.</p>"
                        if not fixtureModes == None:
                            modeResults = ""
                            for m in fixtureModes.keys():
                                temp = fixtureModes[m]
                                modeResults += '<option value="{simpleMode}">{name}</option>'.format(simpleMode=temp.getName().lower(), name=temp.getName())

                            fixtureModeResult = """ 
                            <form action="/FixtureModeChange">
                                <input  type="hidden" id="FixtureName" name="FixtureName" value="{FixtureName}">
                                <select id="modeSelect" name="modeSelect">
                                    {modeResults}
                                </select>
                                <button type="submit">Submit</button>
                            </form>
                            """.format(FixtureName=fixture.getName().lower(), modeResults=modeResults)

                        customReplacements["[FixtureModes]"] = fixtureModeResult
      
      
                    else:
                        failure = True
                        failMessage = "Failed to find the requested fixture."
                else:
                    failure = True
                    failMessage = "No fixture name provided."

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                if failure:
                    self._redirectMessage = failMessage
                    self._redirectURL = "/index"
                    self.wfile.write(bytes(self.replacements(self._redirectPage), "utf-8"))
                else:
                    self.wfile.write(bytes(self.replacements(self._viewFixturePage, customReplacements), "utf-8"))


        """elif cleanPath in ["/ModeChange"]:#OLD Web panel code maybe reused delete later.
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
            self.wfile.write(bytes(self.replacements(self._redirectPage), "utf-8"))"""

    def replacements(self, htmlIn, customReplacements={}):
        if self._controller == None:
            print("Controller failed to be fetched.")
            return htmlIn
    
        for rep in self._replacementDict.keys():
            if htmlIn.find(rep) != -1:
                func = self._replacementDict[rep]
                htmlIn = htmlIn.replace(rep, str(func())) 

        for custom in customReplacements:
            replacement = customReplacements[custom]
            if htmlIn.find(custom) != -1:
                htmlIn = htmlIn.replace(custom, replacement)

        return htmlIn

    #Getters
    def getRedirectURL(self):
        return self._redirectURL

    def getRedirectMessage(self):
        return self._redirectMessage

    def getFixtureList(self):
        result = ""
        fixtures = self._controller.getFixtures()
        for fix in fixtures.keys():
            fixture = fixtures[fix]
            mode = "None"
            if not fixture.getCurrentMode() == None:
                mode = fixture.getCurrentMode().getName()
            result += result + '<tr><td>{name}</td><td>{fixType}</td><td>{fixMode}</td><td><a href="/ViewFixture?fixture={nameLower}">Edit &#8627;</a></td></tr>'.format(name=fixture.getName(), fixType=type(fixture).__name__, fixMode=mode, nameLower=fixture.getName().lower())
        return result

    def getFixtureCount(self):
        return str(len(self._controller.getFixtures()))

    #def htmlModeSettings(self):
    #    controller = self._controller
    #    result = ""
    #    if controller.getCurrentMode() == None:
    #        result = "None"
    #    else:
    #        for s in controller.getCurrentMode().getSettings():
    #            result += '<li><a href="/SettingEdit?settingName={SettingSimpleName}"><p> Edit -> {SettingName}</p></a></li>'.format(SettingSimpleName=s.getName().lower(), SettingName=s.getName())
    #                
    #    return result


    #def do_POST(self):#Should idealy use post request to handle changes. But i can't be arsed too. As this panel is intended to be used in a local network. for personal use i feel i don't need to.
    #    contentLength = int(self.headers["Content-Length"])
    #    postData = self.rfile.read(contentLength).decode("utf-8")

class WebpanelManager(threading.Thread):
    _controller = None
    _dataManager = None
    _webserver = None

    _serverAddress = "localhost"
    _serverPort = 8080

    def __init__(self, dataManager, controller, serverAddress, serverPort, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dataManager = dataManager
        self._controller = controller
        self._serverAddress = serverAddress
        self._serverPort = serverPort

    def run(self):
        hostName = self._serverAddress
        serverPort = self._serverPort

        handler = partial(WebServer, self._dataManager, self._controller)

        self._webServer = HTTPServer((hostName, serverPort), handler)
        print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            self._webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        self._webServer.server_close()
        print("Server stopped.")
