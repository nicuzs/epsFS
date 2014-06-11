import settings
from twisted.conch.checkers import SSHPublicKeyDatabase
from twisted.cred import portal, checkers
from zope.interface import implements
from twisted.conch import avatar
from twisted.conch.interfaces import IConchUser, ISession
from twisted.conch.ssh import keys, session
from twisted.conch.insults import insults
from ssh_protocol import FsepsSshProtocol


def get_host_ssh_keys():
    return ({'ssh-rsa': keys.Key.fromString(data=settings.SSH_PRIVATE_KEY)},
            {'ssh-rsa': keys.Key.fromString(data=settings.SSH_PUBLIC_KEY)})


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
            self, filename=settings.USER_STORAGE_LOCATION, delim=';',
            usernameField=1, passwordField=2)


class FsepsAvatar(avatar.ConchUser):
    implements(ISession)  # I f@*king hate this java-like approach

    def __init__(self, username):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.channelLookup.update({'session': session.SSHSession})

    def openShell(self, protocol):
        serverProtocol = insults.ServerProtocol(FsepsSshProtocol, self)
        serverProtocol.makeConnection(protocol)
        protocol.makeConnection(session.wrapProtocol(serverProtocol))

    def getPty(self, terminal, windowSize, attrs):
        return None

    def windowChanged(self, *args, **kwargs):
        # when the shhclient resizes the window
        pass

    def execCommand(self, protocol, cmd):
        raise NotImplementedError()

    def closed(self):
        pass


class FsepsRealm(object):
    implements(portal.IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IConchUser in interfaces:
            return interfaces[0], FsepsAvatar(avatarId), lambda: None
        else:
            raise NotImplementedError("No supported interfaces found.")
