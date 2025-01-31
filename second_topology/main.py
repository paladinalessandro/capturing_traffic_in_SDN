#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
import subprocess
import time

class NetworkSlicingTopo(Topo):
    def __init__(self):
        #initialize topology
        Topo.__init__(self)

        #create template host,switch and Link

        host_config = dict(inNamespace=True)
        link_config = dict() #total capacity of the link 10Mbps
        host_link_config = dict()

        #create routers nodes - 4 routers in our case
        for i in range(3):
            sconfig = {"dpid": "%016x" % (i+1)}
            self.addSwitch("s%d" % (i+1), **sconfig)

        #create host nodes - 7 host nodes

        self.addHost("dns",ip="10.0.0.10")

        for i in range(1, 4):
            self.addHost("web" + str(i),ip="10.0.0." + str(i))

        #ISP
        self.addHost("r1",ip="10.0.0.5")
        

        #Rete aziendale
        self.addHost("intra",ip="10.0.0.6")

        #add links
        self.addLink("s1", "s2")
        self.addLink("s2", "s3")
        self.addLink("s1", "s3")

        self.addLink("r1", "s1",bw=100)
        self.addLink("web1","s1",bw=50)
        self.addLink("web2","s1",bw=50)
        self.addLink("intra","s3")
        self.addLink("web3","s3",bw=50)
        self.addLink("dns","s2")

        

topos = {"networkslicingtopo": (lambda: NetworkSlicingTopo())}

if __name__=="__main__":
    topo = NetworkSlicingTopo()
    net = Mininet(
        topo=topo,
        controller=RemoteController('c0', ip='127.0.0.1'),
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )

    net.build()
    net.start()
    
    subprocess.call("./total_connectivity.sh")

    webservers = ['web1','web2','web3']
    for i in range(3):
        webserver = webservers[i]
        cmd = "sudo python3 custom_http_server.py &"
        print("Running '{}' at web{}".format(cmd, i+1))
        net.get(webserver).cmd(cmd)
        time.sleep(0.2)

    print("Starting the local DNS service")
    net.get('dns').cmd("python3 dns.py &")
    time.sleep(0.2)

    net.get('intra').cmd("python3 simulator.py &")
    for i in range(20):
        net.get('r1').cmd("python3 simulator.py &")
        
        
    CLI(net)
    net.stop
        