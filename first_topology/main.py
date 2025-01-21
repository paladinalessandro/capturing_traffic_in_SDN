import time
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink

def parse_args(parser):
    parser.add_argument("-k", type=int, default=1,
                        help="Create a topology with k webservers")
    return parser.parse_args()

def createNetwork(k=3):
    net = Mininet(controller=Controller, switch=OVSKernelSwitch, link=TCLink)

    info('*** Adding controller\n')
    controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    net.addController(controller)

    webservers = []
    for i in range(1, k+1):
        webservers.append(net.addHost('web' + str(i),ip='10.0.0.' + str(i)))
    dns = net.addHost('dns',ip='10.0.0.10')

    info('*** Adding switches\n') 
    switches = []
    for i in range(1, 5):
        switches.append(net.addSwitch('s' + str(i), cls=OVSKernelSwitch, protocols='OpenFlow13'))


    info('*** Adding routers\n')
    r1 = net.addHost('r1')
    r2 = net.addHost('r2')

    #Rete aziendale
    intra = net.addHost('intra')

    info('*** Creating links\n')
    # Router & Switch links
    net.addLink(switches[0], r1,bw=100*8, delay='10ms', max_queue_size=1000)
    net.addLink(switches[0], intra)
    net.addLink(switches[0], switches[2], delay='9ms', max_queue_size=1000)

    net.addLink(switches[1], r2,bw=70*8, delay='14ms', max_queue_size=1000)
    net.addLink(switches[1], switches[2], delay='12ms', max_queue_size=1000)
    net.addLink(switches[1], switches[3], delay='11ms', max_queue_size=1000)

    net.addLink(switches[3], dns)

    # Switch to Host links
    for i in range(0, k):
        net.addLink(switches[2], webservers[i],bw=50*8)

    info('*** Starting network\n')
    net.start()
    for i in range(k):
        webserver = webservers[i]
        cmd = "sudo python3 custom_http_server.py &"
        print("Running '{}' at web{}".format(cmd, i+1))
        webserver.cmd(cmd)
        time.sleep(0.2)
    print("Starting the local DNS service")
    dns.cmd("python3 dns.py &")
    time.sleep(0.2)

    intra.cmd("python3 simulator.py &")
    for i in range(20):
        r1.cmd("python3 simulator.py &")

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    createNetwork()