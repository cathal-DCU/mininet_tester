import http.server
import socketserver
import sys
import time

import Network

# Server handler
class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def handle_one_request(self):
        time.sleep(0.1)	
        return http.server.SimpleHTTPRequestHandler.handle_one_request(self)


# Loop until shutdown
httpd = socketserver.TCPServer(("", Network.ServerPort), ServerHandler)
while True:
    httpd.handle_request()