import sys
import os
import pwd

from settings import RUN_CFG_DEFAULT, FILE_SYS_PATH
from fuse import FUSE

if __name__ == '__main__':
    """
        simple interface to manually mount the filesystem; this shouldn't ever
        be run by root since the mount operation is user-specific
    """

    cfg = RUN_CFG_DEFAULT

    try:
        username = sys.argv[1]
    except IndexError:
        uid = os.geteuid()
        if uid == 0:
            print "Root user shouldn't mount the filesystem"
            exit(1)
        username = pwd.getpwuid(uid).pw_name

    if username == 'root':  # paranoic check
        print "Root user shouldn't mount the filesystem"
        exit()

    cfg['mountpoint'] = cfg['mountpoint'] % username

    #save  the current pid so we can SIGINT to unmount
    f = open('%sunmount/%s_mount.pid' % (FILE_SYS_PATH, username), 'w')
    f.write(str(os.getpid()))
    f.close()

    FUSE(**cfg)

