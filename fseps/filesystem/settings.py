ABSOLUTE_FILESYSTEM_PATH = '/home/nicu/Dropbox/kernel/fseps/file_sys/'

FILESYSTEM_ROOT = '%sfs_root/' % ABSOLUTE_FILESYSTEM_PATH
FILESYSTEM_MOUNTPOINT = '/fseps/'

FSEPS_CONFIG_USR = '%susers.data' % ABSOLUTE_FILESYSTEM_PATH
FSEPS_CONFIG_GRP = '%sgroups.data' % ABSOLUTE_FILESYSTEM_PATH

RUN_CFG_DEFAULT = {
    'operations': None,     # Must add here an instance of my Operation set
    'mountpoint': FILESYSTEM_MOUNTPOINT,
    'foreground': True,
    'allow_other': True,
}

FSEPS_PERMISSIONS_FILE_NAME = '.,fseps'
