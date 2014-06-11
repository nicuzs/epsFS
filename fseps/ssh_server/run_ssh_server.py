import sys

# from twisted.cred import portal, checkers
from twisted.conch.ssh import factory
from twisted.internet import reactor
from twisted.python import log

from sshserver_spine import *

log.startLogging(sys.stderr)
# log.startLogging(open('/home/nicu/dev/logs/fseps/ssh_server.log', 'w'))


if __name__ == '__main__':
    sshFactory = factory.SSHFactory()
    sshFactory.portal = portal.Portal(FsepsRealm())
    sshFactory.portal.registerChecker(PasswdUsersDb())
    sshFactory.portal.registerChecker(SshUsersDb())
    sshFactory.privateKeys, sshFactory.publicKeys = get_host_ssh_keys()
    reactor.listenTCP(8022, sshFactory)
    reactor.run()
