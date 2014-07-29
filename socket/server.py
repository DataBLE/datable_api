import json
from twisted.application import service, internet
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

#TODO: Take these values in as cmdline params
MOTE_PORT=9090  # Incoming mote connections
CLOUD_PORT=9091 # Incoming cloud connections


class CloudReceiver(LineReceiver):
    '''Receives \n delimited JSON from cloud, and pipes to appropriate mote'''
    delimiter = '\n'

    def lineReceived(self, line):
        print line
        data = json.loads(line)
        addr = '%s:%s:%s' % (data.get('uuid',None), 
                data.get('major',None), data.get('minor', None))
        mote = self.proxy.connected_motes.get(addr, None)
        if mote:
            mote.transport.write(line+'\n')
        else:
            print "mote not found: %s" % addr

class CloudReceiverFactory(Factory):
    '''Builds instances of CloudReceiver protocols'''
    def buildProtocol(self, addr):
        proto = CloudReceiver()
        proto.proxy = self.proxy
        return proto


class MoteReceiver(LineReceiver):
    '''Receives \n delimited string from motes for ID, and is used
    to send JSON data to motes'''
    delimiter = '\n'

    def connectionMade(self,):
        print 'connectionMade'
        self.uuid = None
        self.major = None
        self.minor = None

    def lineReceived(self, line):
        print line
        # The mote is identifying itself store in dictionary
        self.uuid, self.major, self.minor = line.split(':')
        # Add ourselves to connected_motes
        self.proxy.connected_motes[line] = self

    def connectionLost(self, reason):
        print 'connectionLost'
        # Remove ourselves from connected_motes
        del self.proxy.connected_motes['%s:%s:%s' % 
                (self.uuid, self.major, self.minor)]


class MoteReceiverFactory(Factory):
    '''Builds instances of MoteReceiver protocols'''
    def buildProtocol(self, addr):
        proto = MoteReceiver()
        proto.proxy = self.proxy
        return proto


class ProxyService(service.Service):
    '''Listens for connections from cloud servers, and pipes received data
    to appropriate connected mote'''
    def startService(self,):
        self.connected_motes = {} # key=uuid:major:minor, value=transport
        cf = CloudReceiverFactory()
        cf.proxy = self
        mf = MoteReceiverFactory()
        mf.proxy = self
        self.mote_server = reactor.listenTCP(MOTE_PORT, mf)
        self.cloud_server = reactor.listenTCP(CLOUD_PORT, cf)

    def stopService(self,):
        self.cloud_server.stopListening()
        self.mote_server.stopListening()
        self.connected_motes = None

application = service.Application('MOTE command proxy')
multiservice = service.MultiService()
service = ProxyService()
service.setServiceParent(application)
