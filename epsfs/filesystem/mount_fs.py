from settings import RUN_CFG_DEFAULT, FILESYSTEM_ROOT
from fuse import FUSE
from epsFSOperations import EpsFSOperations

if __name__ == '__main__':
    print "Filesystem mounted in -->%s" % RUN_CFG_DEFAULT['mountpoint']
    RUN_CFG_DEFAULT['operations'] = EpsFSOperations(root=FILESYSTEM_ROOT)
    FUSE(**RUN_CFG_DEFAULT)

