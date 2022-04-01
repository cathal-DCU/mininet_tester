import requests
import sys

import Network

i = 100
f = open("./log/log-" + sys.argv[1] + ".txt", "a")
while i > 0:
	# Make request to load balancing node
	requestAddress = "http://{}:{}".format(Network.LoadBalacingNodes[0], Network.LoadBalancingPort)
	x = requests.get(requestAddress)

	print("Writing elapsed...")

	# Write out request duration
	f.write(str(x.elapsed.total_seconds())+"\n")
	i = i - 1


