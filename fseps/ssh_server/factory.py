import settings
from twisted.conch.ssh import keys, factory, userauth, connection
from twisted.conch.checkers import SSHPublicKeyDatabase
from twisted.cred import portal, checkers
from zope.interface import implements
from twisted.conch import error, avatar
from twisted.internet import protocol
from twisted.conch.ssh import keys, session
from twisted.conch.insults import insults

class FsepsFactory(factory.SSHFactory):
    def __init__(self, *args, **kwargs):
        FsepsFactory.portal = kwargs['portal']  # i don't use `get` so it breaks

    publicKeys = {
        'ssh-rsa': keys.Key.fromString(data=settings.SSH_PUBLIC_KEY)
    }
    privateKeys = {
        'ssh-rsa': keys.Key.fromString(data=settings.SSH_PRIVATE_KEY)
    }
    services = {
        'ssh-userauth': userauth.SSHUserAuthServer,
        'ssh-connection': connection.SSHConnection
    }


class SshUsersDb(SSHPublicKeyDatabase):
    def checkKey(self, credentials):
        saved_keys = {
            'nicu': keys.Key.fromString(data=settings.SSH_PUBLIC_KEY).blob(),

        }
        return bool(len([username for username, key in saved_keys.items()
                         if (credentials.username == username and
                             key == credentials.blob)]))


class PasswdUsersDb(checkers.FilePasswordDB):
    def __init__(self):
        """
            sorry OOP but i cannot use super here because twisted was written
            by some dumb Java lovers who do not know how to subclass `object`
        """
        checkers.FilePasswordDB.__init__(
            self, filename=settings.USER_STORAGE_LOCATION, delim=';')


class FsepsAvatar(avatar.ConchUser):
    def __init__(self, username):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.channelLookup.update({'session': session.SSHSession})


class FsepsRealm:
    implements(portal.IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        return interfaces[0], FsepsAvatar(avatarId), lambda: None


class FsepsProtocol(protocol.Protocol):
    def __init__(self, user):
        self.user = user
    def dataReceived(self, data):
        # import ipdb; ipdb.set_trace()

        if data == '\r':
            data = '\r\n'
        elif data == '\x03':  # ^C
            self.transport.loseConnection()
            return
        self.transport.write(data)

