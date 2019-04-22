import neonet_routing_layer as nrl
import neonet_raw as ntl
import time
from netcrypt import sha512, encrypt1, decrypt1

# this module's purpose is to connect to neonet and establish connections.
# it does not (easily) support more advanced setups, like network switches between different types of hardware.

millis = ntl.millis

address = nrl.rand_addr(False)

DEFAULT_TCP_SERVERS = [('68.5.129.54',1155)]#,('192.168.0.1',16927)]

man = None

_is_setup = False
def setup(adr=address, tcp_servers = DEFAULT_TCP_SERVERS, routing_table={nrl.DEFAULT_AREA_CODE:0}):
    global address, man, _is_setup
    if _is_setup:
        return "Already set up!"
    address = adr
    man = nrl.NrlConnectionManager(address,routing_table)
    man.startUpdateThread()
    for i in tcp_servers:
        man.addUplink(ntl.TcpClientUplink(i[0],i[1]))
    _is_setup = True
class NrlConnection:
    def __init__(self, adr, port):
        self.adr=adr
        self.port=port
        self.queue = []
    def send(self,data):
        if man==None:
            return False
        return man.sendPacket(self.adr,self.port, data)
    def recv(self,timeout = 8000):
        if self.available()>0:
            return self.queue.pop()
        else:
            timer = ntl.millis()+timeout
            while timer>ntl.millis():
                if self.available()>0:
                    return self.queue.pop()
                time.sleep(0.0001)
            return None
    def available(self):
        if man==None:
            return len(self.queue)
        i=0
        while i<len(man.queue):
            if man.queue[i][0]==self.adr and man.queue[i][1]==self.port:
                self.queue.insert(0,man.queue.pop(i)[2])
            else:
                i+=1
        return len(self.queue)

class NrlOpenPort:
    def __init__(self, port):
        self.port=port
        self.queue = []
    def send(self, adr, data):
        if man==None:
            return False
        return man.sendPacket(adr,self.port, data)
    def recv(self,timeout = 8000):
        if self.available()>0:
            return self.queue.pop()
        else:
            timer = ntl.millis()+timeout
            while timer>ntl.millis():
                if self.available()>0:
                    return self.queue.pop()
                time.sleep(0.0001)
            return None
    def available(self):
        if man==None:
            return len(self.queue)
        i=0
        man.update()
        while i<len(man.queue):
            if man.queue[i][1]==self.port:
                pk = man.queue.pop(i)
                self.queue.insert(0,[pk[0],pk[2]])
            else:
                i+=1
        return len(self.queue)

class NrlSecureConnection:
    def __init__(self, adr, port, key, timeout=1000): # set timeout to null to await a connection
        self.adr=adr
        self.port=port
        self.queue = []
        self.key = key

        timer = float('inf')
        if timeout!=None:
            timer = timeout+millis()
        # do handshake
        self.verif = sha512(key)
        self.send(self.verif)
        while millis()<timer:
            inval = self.recv(timer-millis())
            if inval!=None:
                if inval==self.verif:
                    self.send(self.verif)   # be sure they know that we got the message
                    if self.recv()!=self.verif:
                        raise Exception("Handshake Aborted Unexpectedly Error")
                    return
                else:
                    print(inval)
                    raise Exception("Invalid Key Error")
                    #break
        raise Exception("No Response Error")
    def send(self,data):
        if man==None:
            return False
        return man.sendPacket(self.adr,self.port, encrypt1(data, self.key))
    def recv(self,timeout = 8000):
        if self.available()>0:
            return self.queue.pop()
        else:
            timer = millis()+timeout
            while timer>millis():
                if self.available()>0:
                    return self.queue.pop()
                time.sleep(0.0001)
            return None
    def available(self):
        if man==None:
            return len(self.queue)
        i=0
        while i<len(man.queue):
            if man.queue[i][0]==self.adr and man.queue[i][1]==self.port:
                try:
                    data = decrypt1(man.queue.pop(i)[2], self.key)
                    self.queue.insert(0,data)
                except:
                    pass
            else:
                i+=1
        return len(self.queue)
