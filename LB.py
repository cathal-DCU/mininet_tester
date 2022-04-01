from importlib.resources import path
import time
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
import sys
import os

import Network

def StartLoadTest(net, topology, lbAlgorithm):

    print("\n--> Starting load test...")

    # Get ClientNode script path
    clientNodeScriptPath = os.path.join(os.path.dirname(__file__), "ClientNode.py")

    # Run client nodes c1, c2 in background - wait on c3
    net.get("c1").cmd("python {} {} {} {} &".format(clientNodeScriptPath, "c1", topology, lbAlgorithm))
    net.get("c2").cmd("python {} {} {} {} &".format(clientNodeScriptPath, "c2", topology, lbAlgorithm))
    net.get("c3").cmd("python {} {} {} {}".format(clientNodeScriptPath, "c3", topology, lbAlgorithm))

    # Allow time for files to flush
    time.sleep(4)

    # Monitor load balancing node
    net.get("lb").monitor()
    print("---> Done")
    return

def CheckLoadBalancingAlgorithm(algorithm):
    return algorithm in Network.LoadBalancingAlgorithms



if __name__ == '__main__':
    
    # Set log level
    setLogLevel( 'info' )

    # Create net
    net = Mininet(topo=None, build=False, link=TCLink, ipBase='10.0.0.0/8')

    # Check for enough arguments
    if len(sys.argv) >= 3:
        
        # Get arguments
        topology = sys.argv[1]
        lbAlgorithm = sys.argv[2]
        print(topology)
        print(lbAlgorithm)

        if topology == "star":
            if CheckLoadBalancingAlgorithm(lbAlgorithm):
                Network.CreateStarNetworkTopology(net, lbAlgorithm)
                StartLoadTest(net, topology, lbAlgorithm)
                CLI(net)
            else:
                print("Unrecognised load balancing algorithm, return to CLI")
                CLI(net)
        elif topology == "tree":
            
            if CheckLoadBalancingAlgorithm(lbAlgorithm):
                Network.CreateTreeNetworkTopology(net, lbAlgorithm)
                StartLoadTest(net, topology, lbAlgorithm)
                CLI(net)
            else:
                print("Unrecognised load balancing algorithm, return to CLI")
                CLI(net)
        else:
            print("Unrecognised topology, return to CLI")
            CLI(net)
    else:
        print("Please specify topology and load balancing algorithm, return to CLI")
        CLI(net)