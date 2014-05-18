import sys
# import argparse # TODO must add a pretty CLI menu
from fuse import FUSE
from fseps import FsEps

RUN_CFG_DEFAULT = {
    'operations': FsEps(root='fs_root'),
    'mountpoint': 'mnt_point',
    'foreground': True
}

RUN_CFG_DEBUG = {
    'operations': FsEps(root='fs_root'),
    'mountpoint': 'mnt_point',
    'foreground': True,
    'debug': True
}

if __name__ == '__main__':
    cfg = RUN_CFG_DEBUG if len(sys.argv) == 2 and sys.argv[1] == 'd' \
        else RUN_CFG_DEFAULT
    if not cfg.get('debug'):
        print('\n->Started using the default config')
    FUSE(**cfg)
