import requests
import sys
import os
from mininet.log import setLogLevel, info

import Network

# Set defaults
maxRequestCount = 100

# Create file name
fileName = "./log/log-" + sys.argv[1] + "-" + sys.argv[2] + "-" + sys.argv[3] + ".txt"
directoryName = os.path.dirname(fileName)

# Create directory if not exists
if not os.path.exists(directoryName):
	os.makedirs(directoryName)
# Print file name
print(fileName)

# Write out each request elapsed time to file
with open(fileName, "w") as file:
	for i in range(maxRequestCount):

		# Make request to load balancing node
		requestAddress = "http://{}:{}".format(Network.LoadBalacingNodes[0], Network.LoadBalancingPort)
		x = requests.get(requestAddress)

		#info("*** " + sys.argv[1] + " - Writing elapsed - {} - {}\n".format(i, str(x.elapsed.total_seconds())))
		#print("*** " + sys.argv[1] + " - Writing elapsed - {} - {}".format(i, str(x.elapsed.total_seconds())))

		# Write out request duration
		file.write(str(x.elapsed.total_seconds())+"\n")