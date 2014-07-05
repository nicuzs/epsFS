ABSOLUTE_FILESYSTEM_PATH = '/home/nicu/Dropbox/kernel/epsFS/file_sys/'

FILESYSTEM_ROOT = '%sfs_root/' % ABSOLUTE_FILESYSTEM_PATH
FILESYSTEM_MOUNTPOINT = '/epsfs/'

EPSFS_CONFIG_USR = '%susers.,epsfs' % ABSOLUTE_FILESYSTEM_PATH
EPSFS_CONFIG_GRP = '%sgroups.,epsfs' % ABSOLUTE_FILESYSTEM_PATH

RUN_CFG_DEFAULT = {
    'operations': None,     # Must add here an instance of my Operation set
    'mountpoint': FILESYSTEM_MOUNTPOINT,
    'foreground': True,
    'allow_other': True,
}

EPSFS_PERMISSIONS_FILE_NAME = ',epsfs'

EPSFS_AND = '<and>'
EPSFS_OR = '<or>'
