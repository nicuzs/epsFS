from settings import RUN_CFG_DEFAULT, FILESYSTEM_ROOT
from fuse import FUSE
from fseps import FsEps

if __name__ == '__main__':
    print "Filesystem mounted in -->%s" % RUN_CFG_DEFAULT['mountpoint']
    RUN_CFG_DEFAULT['operations'] = FsEps(root=FILESYSTEM_ROOT)
    FUSE(**RUN_CFG_DEFAULT)

