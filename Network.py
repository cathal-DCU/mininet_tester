import os
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf


# Network address details
Servers = ["10.0.0.1", "10.0.0.2"]
ServerPort = 8080
LoadBalacingNodes = ["10.0.0.3"]
LoadBalancingPort = 9090
LoadBalancingAlgorithms = ["rr", "random", "none"]
Clients = ["10.0.0.4", "10.0.0.5", "10.0.0.6"]


# Adds custom server and load balancing handlers
def AddCustomHandlers(net, lbAlgorithm):
    
    # Setup server handlers in the background
    serverHandlerScriptPath = os.path.join(os.path.dirname(__file__), "ServerHandler.py")
    net.get("serv1").sendCmd("python {} &".format(serverHandlerScriptPath))
    net.get("serv2").sendCmd("python {} &".format(serverHandlerScriptPath))

    # Setup load balancing node in the background
    loadBalancingNodeScriptPath = os.path.join(os.path.dirname(__file__), "LoadBalancingNode.py")
    net.get("lb").sendCmd("python {} {} &".format(loadBalancingNodeScriptPath, lbAlgorithm))
    


# The code creates a network with 3 clients, 1 load balancer, 2 servers and 1 switch.
# The clients are connected to the switch with a bandwidth of 1Mbps.
# The switch is connected to the servers with a bandwidth of 4Mbps.
# The switch is connected to the load balancer with a bandwidth of 10Mbps.
# The switch is connected to the controller with a bandwidth of 10Mbps.
def CreateStarNetworkTopology(net, lbAlgorithm):

    # Creating star network topology
    info( '*** Creating star network topology...\n' )

    # Create network controllers
    info( '*** Adding controllers...\n' )
    con1 = net.addController(name='con1',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    # Create switches
    info( '*** Adding switches...\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    # Create servers
    info( '*** Adding servers...\n')
    serv1 = net.addHost('serv1', cls=Host, ip=Servers[0], defaultRoute=None)
    serv2 = net.addHost('serv2', cls=Host, ip=Servers[1], defaultRoute=None)

    # Connect servers to switch
    info( '*** Connecting servers to switch...\n')
    net.addLink(serv1, s1, bw=4)
    net.addLink(serv2, s1, bw=4)

    # Create load balancing nodes
    info( '\n*** Adding load balancing nodes...\n')
    lb = net.addHost('lb', cls=Host, ip=LoadBalacingNodes[0], defaultRoute=None, cpu=0.2)

    # Connect load balancing nodes to switch
    info( '*** Connecting load balancing nodes to switch...\n')
    net.addLink(lb, s1, bw=10)

    # Create clients
    info( '\n*** Adding clients...\n')
    c1 = net.addHost('c1', cls=Host, ip=Clients[0], defaultRoute=None, cpu=0.2)
    c2 = net.addHost('c2', cls=Host, ip=Clients[1], defaultRoute=None, cpu=0.2)
    c3 = net.addHost('c3', cls=Host, ip=Clients[2], defaultRoute=None, cpu=0.2)
    
    # Connect clients to switch
    info( '*** Connecting clients to switch...\n')
    net.addLink(c1, s1, bw=1)
    net.addLink(c2, s1, bw=1)
    net.addLink(c3, s1, bw=1)

    # Start network
    info( '\n*** Starting network...\n')
    net.build()
    
    # Start controllers
    info( '*** Starting controllers...\n')
    for controller in net.controllers:
        controller.start()

    # Start switches
    info( '*** Starting switches...\n')
    net.get('s1').start([con1])

    # Add custom handlers
    AddCustomHandlers(net, lbAlgorithm)
    

# The code creates a network with 3 clients, 1 load balancer, 2 servers and 3 switches.
# The clients are connected to the switch with a bandwidth of 1Mbps.
# The switch is connected to the servers with a bandwidth of 10Mbps.
# The switch is connected to the load balancer with a bandwidth of 10Mbps.
def CreateTreeNetworkTopology(net, lbAlgorithm):

    # Creating tree network topology
    info( '*** Creating tree network topology...\n' )

    # Create network controllers
    info( '*** Adding controllers...\n' )
    con1=net.addController(name='con1',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)
        
    con2=net.addController(name='con2',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    con3=net.addController(name='con3',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    # Create switches
    info( '*** Adding switches...\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)

    # Connect switches
    info( '*** Connecting switches to switches...\n')
    net.addLink(s1, s3, bw=2)
    net.addLink(s2, s3, bw=2)

    # Create servers
    info( '\n*** Adding servers...\n')
    serv1 = net.addHost('serv1', cls=Host, ip=Servers[0], defaultRoute=None)
    serv2 = net.addHost('serv2', cls=Host, ip=Servers[1], defaultRoute=None)

    # Connect servers
    info( '*** Connecting servers to switches...\n')
    net.addLink(serv1, s3, bw=10)
    net.addLink(serv2, s3, bw=10)

    # Create load balancing nodes
    info( '\n*** Adding load balancing nodes...\n')
    lb = net.addHost('lb', cls=Host, ip=LoadBalacingNodes[0], defaultRoute=None, cpu=0.2)

    # Connect load balancing nodes to switch
    info( '*** Connecting load balancing nodes to switch...\n')
    net.addLink(lb, s3, bw=10)

    # Create clients
    info( '\n*** Adding clients...\n')
    c1 = net.addHost('c1', cls=Host, ip=Clients[0], defaultRoute=None, cpu=0.2)
    c2 = net.addHost('c2', cls=Host, ip=Clients[1], defaultRoute=None, cpu=0.2)
    c3 = net.addHost('c3', cls=Host, ip=Clients[2], defaultRoute=None, cpu=0.2)

    # Connect clients to switch
    info( '*** Connecting clients to switches...\n')
    net.addLink(c1, s1, bw=1)
    net.addLink(c2, s1, bw=1)
    net.addLink(c3, s2, bw=1)

    # Start network
    info( '\n*** Starting network...\n')
    net.build()

    # Start controllers
    info( '*** Starting controllers...\n')
    for controller in net.controllers:
        controller.start()

    # Start switches
    info( '*** Starting switches...\n')
    net.get('s1').start([con1])
    net.get('s2').start([con2])
    net.get('s3').start([con3])

    # Add custom handlers
    AddCustomHandlers(net, lbAlgorithm)