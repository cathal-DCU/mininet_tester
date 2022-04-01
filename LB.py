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

import Network


def StartLoadTest(net):

    print("\n--> Starting load test...")

    # Setup client nodes
    net.get("c1").cmd("python ./ClientNode.py")
    net.get("c2").cmd("python ./ClientNode.py")
    net.get("c3").cmd("python ./ClientNode.py")

    time.sleep(4)

    # Monitor load balancing node
    net.get("lb").monitor()
    print("---> Done")
    return



if __name__ == '__main__':
    
    # Set log level
    setLogLevel( 'info' )

    # Create net
    net = Mininet(topo=None, build=False, link=TCLink, ipBase='10.0.0.0/8')

    # Check for topology argument
    if len(sys.argv) >= 2:		
        if sys.argv[1] == "star":
            Network.CreateStarNetworkTopology(net)
            # net.pingAll()
            # net.iperf()
            StartLoadTest(net)
            #testbase(net)
            CLI(net)
        elif sys.argv[1] == "tree":
            Network.CreateTreeNetworkTopology(net)
            # net.pingAll()
            # net.iperf()
            StartLoadTest(net)
            CLI(net)
    else:
        print("Unrecognised topology, return to CLI")
        CLI(net)
    
    # Stop network
    net.stop()