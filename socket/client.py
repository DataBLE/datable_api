'''Run this on remote motes so they can receive commands'''
import json
import os
from twisted.application import service, internet
from twisted.internet import reactor
from twisted.internet.utils import getProcessOutput
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.protocols.basic import LineReceiver

#TODO: Take these values in as cmdline params
UUID='2F234454-CF6D-4A0F-ADF2-F4911BA9FFA6'
MAJOR='1'
MINOR='1'
HOST='174.129.231.63'
#HOST='localhost'
PORT=9090
MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')



class MoteListener(LineReceiver):
    '''Receives \n delimited JSON, and executes command as a process'''
    delimiter = '\n'

    def __init__(self, uuid, major, minor):
        self.uuid = uuid
        self.major = major
        self.minor = minor

    def connectionMade(self,):
        self.factory.resetDelay() # Reset factory delay
        # Let the server know what mote we are
        self.transport.write('%s:%s:%s\n' % (self.uuid, self.major, self.minor))

    def lineReceived(self, line):
        print line
        data = json.loads(line)
        action = data.get('action', None)
        resource = data.get('resource', None)
        if action == 'tv-video':
            output = getProcessOutput('/usr/bin/omxplayer', 
                    args=(os.path.join(MEDIA_DIR,resource),), 
                    errortoo=True)
        elif action == 'tv-image':
            output = getProcessOutput('/usr/bin/fim',
                    args=(os.path.join(MEDIA_DIR,resource), '-a'),
                    errortoo=True)
            print(output)



class MoteListenerFactory(ReconnectingClientFactory):
    '''Builds instances of Mote protocols'''
    def buildProtocol(self, addr):
        proto = MoteListener(uuid=UUID, major=MAJOR, minor=MINOR)
        proto.factory = self # Keep a ref to the factory
        return proto


application = service.Application('MOTE command receiver')
service = internet.TCPClient(HOST, PORT, MoteListenerFactory())
service.setServiceParent(application)
