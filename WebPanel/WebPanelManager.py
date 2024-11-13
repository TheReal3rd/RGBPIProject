#Sources:
#   https://pythonbasics.org/webserver/

from http.server import BaseHTTPRequestHandler, HTTPServer

import _thread
import threading
import time

class WebServer(BaseHTTPRequestHandler):
    _pagesLoaded = False

    _indexPage = None 

    def loadPages(self):
        indexReader = open("WebPanel/HTML/index.html", "r")
        self._indexPage = indexReader.read()
        self._pagesLoaded = True

    def do_GET(self):
        if not self._pagesLoaded:
            self.loadPages()

        if self.path in ["/", "index.html"]:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(self._indexPage, "utf-8"))

        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><head><title>Error</title></head>", "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes("<p>404 Page not found.</p>", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))

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


        self._webServer = HTTPServer((hostName, serverPort), WebServer)
        print("Server started http://%s:%s" % (hostName, serverPort))

        try:
            self._webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        self._webServer.server_close()
        print("Server stopped.")
