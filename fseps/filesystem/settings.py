import os
import getpass
from fseps import FsEps

ABSOLUTE_FILESYSTEM_PATH = '/home/nicu/Dropbox/kernel/fseps/file_sys/'

FILESYSTEM_ROOT = '%sfs_root/' % ABSOLUTE_FILESYSTEM_PATH
FILESYSTEM_MOUNTPOINT = '/home/fseps/'

FSEPS_CONFIG_USR = '%susers.data' % ABSOLUTE_FILESYSTEM_PATH
FSEPS_CONFIG_GRP = '%sgroups.data' % ABSOLUTE_FILESYSTEM_PATH

RUN_CFG_DEFAULT = {
    'operations': FsEps(root=FILESYSTEM_ROOT),
    'mountpoint': FILESYSTEM_MOUNTPOINT,
    'foreground': True
}
