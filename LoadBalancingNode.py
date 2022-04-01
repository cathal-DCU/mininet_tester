import http.server
import socketserver
import sys
import random

import Network

def SelectByRoundRobin(c, serverAddresses):
	n = c % len(serverAddresses)
	return serverAddresses[n]

def SelectByRandom(serverAddresses):
	n = random.randint(0,1)
	return serverAddresses[n]

class LoadBalancingNodeHandler(http.server.SimpleHTTPRequestHandler):
	serverAddresses = []    
	for i in range(len(Network.Servers)):
		serverAddresses.append("http://{}:{}".format(Network.Servers[i], Network.ServerPort))

	def do_GET(self):
		global requestCount

		# Send redirect response
		self.send_response(301)

		# Select redirect address
		if (sys.argv[1] == "rr"):
			add = SelectByRoundRobin(requestCount, self.serverAddresses)
		elif (sys.argv[1] == "random"):
			add = SelectByRandom(self.serverAddresses)
		else:
			add = self.serverAddresses[0]

		# Increment request count
		requestCount = requestCount + 1

		# Redirect to selected server
		self.send_header('Location', add)
		self.end_headers()

requestCount = 0
server = socketserver.TCPServer(("", Network.LoadBalancingPort), LoadBalancingNodeHandler)
server.serve_forever()