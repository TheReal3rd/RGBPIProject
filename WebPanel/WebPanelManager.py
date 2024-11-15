#Sources:
#   https://pythonbasics.org/webserver/
#   https://stackoverflow.com/questions/21631799/how-can-i-pass-parameters-to-a-requesthandler

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

        if cleanPath in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(self.replacements(self._indexPage), "utf-8"))

        elif cleanPath in ["/ModeChange.html"]:
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
            self._redirectURL = "/index.html"
            self.wfile.write(bytes(self.replacements(self._redirectPage), "utf-8"))

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self._redirectMessage = "404 Page not found."
            self._redirectURL = "/index.html"
            self.wfile.write(bytes(self.replacements(self._redirectPage), "utf-8"))

    def replacements(self, htmlIn):
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
        
        return htmlIn

    #def do_POST(self):
    #    contentLength = int(self.headers["Content-Length"])
    #    postData = self.rfile.read(contentLength).decode("utf-8")

#47
#Working but incomplete.
class WebpanelManager(threading.Thread):
    _controller = None
    _webserver = None

    def __init__(self, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._controller = controller

    def run(self):
        hostName = "localhost"
        serverPort = 8080

        handler = partial(WebServer, self._controller)

        self._webServer = HTTPServer((hostName, serverPort), handler)
        print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            self._webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        self._webServer.server_close()
        print("Server stopped.")
