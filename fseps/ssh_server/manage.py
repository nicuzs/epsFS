import sys
import os

from fuse import FUSE
from fseps import FsEps

RELATIVE_ROOT = '../dir/fs_root'
RELATIVE_MOUNT = '../dir/mnt_point/'

RUN_CFG_DEFAULT = {
    'operations': FsEps(root=os.path.join(os.getcwd(), RELATIVE_ROOT)),
    'mountpoint': os.path.join(os.getcwd(), RELATIVE_MOUNT),
    'foreground': True
}

RUN_CFG_DEBUG = {
    'operations': FsEps(root=os.path.join(os.getcwd(), RELATIVE_ROOT)),
    'mountpoint': os.path.join(os.getcwd(), RELATIVE_MOUNT),
    'foreground': True,
    'debug': True
}

if __name__ == '__main__':
    cfg = RUN_CFG_DEBUG if len(sys.argv) == 2 and sys.argv[1] == 'd' \
        else RUN_CFG_DEFAULT

    if cfg == RUN_CFG_DEFAULT:
        print('\n->Started using the default config')
    elif cfg == RUN_CFG_DEBUG:
        print('\n->Started using the debug config')

    FUSE(**cfg)

