import sys

from twisted.cred import portal, checkers

from twisted.conch.ssh import session
from twisted.internet import reactor

from twisted.python import log
from twisted.python import components

from factory import FsepsFactory, SshUsersDb, PasswdUsersDb, FsepsAvatar, \
    FsepsProtocol, FsepsRealm

log.startLogging(sys.stderr)
# log.startLogging(open('/home/nicu/dev/logs/fseps/ssh_server.log', 'w'))


class FsepsSession:
    def __init__(self, avatar, *args, **kwargs):
        self.cmd = None
        self.proto = None
        self.ptyReq = False
        self.eof = 0
        """
        We don't use it, but the adapter is passed the avatar as its first
        argument.
        """

    def getPty(self, term, windowSize, attrs):
        # import ipdb; ipdb.set_trace()
        print "getPty ---<<"
        self._terminalType = term
        self._windowSize = windowSize
        self.ptyReq = True

    def execCommand(self, proto, cmd):
        import ipdb; ipdb.set_trace()
        self.cmd = cmd
        raise Exception("no executing commands")

    def openShell(self, trans):
        # import ipdb; ipdb.set_trace()

        ep = FsepsProtocol()
        ep.makeConnection(trans)
        trans.makeConnection(session.wrapProtocol(ep))

    def eofReceived(self):
        self.eof = 1

    def closed(self):
        log.msg('closed cmd ------------>"%s"' % self.cmd)
        # self.remoteWindowLeftAtClose = self.proto.session.remoteWindowLeft
        # self.onClose.callback(None)


components.registerAdapter(FsepsSession, FsepsAvatar, session.ISession)
portal = portal.Portal(FsepsRealm())
portal.registerChecker(PasswdUsersDb())
portal.registerChecker(SshUsersDb())

if __name__ == '__main__':
    reactor.listenTCP(8022, FsepsFactory(portal=portal))
    reactor.run()
