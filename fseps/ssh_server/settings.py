import os
import getpass
from fseps import FsEps

FILE_SYS_PATH = '/home/nicu/Dropbox/kernel/fseps/file_sys/'
# TODO find a way to get this the right way - using os.join ...

RELATIVE_ROOT = '%sfs_root/' % FILE_SYS_PATH
ABSOLUTE_MOUNTPOINT_PATH = '/home/%s/media/'  # for the ssh user


FILESYSTEM_SOURCE_ROOT = RELATIVE_ROOT

RUN_CFG_DEFAULT = {
    'operations': FsEps(root=RELATIVE_ROOT),
    'mountpoint': ABSOLUTE_MOUNTPOINT_PATH,
    'foreground': True
}

USER_STORAGE_LOCATION = '%susers.data' % FILE_SYS_PATH

SSH_SERVER_WELCOME_MSG = """
*****************************************************************
  ,           ,         __|   __|  __|  _ \   __|
 /             \\        _|  \__ \  _|   __/ \__ \\
((__-^^-,-^^-__))      _|   ____/ ___| _|   ____/
 `-_---' `---_-'
  `--|o` 'o|--'   FSEPS shh server
     \  `  /      Copyright (C) 2014 NiCU Natrapeiu
      ): :(       This is free software, and you are welcome
      :o_o:       to redistribute it under certain conditions
       "-"        i.e. GNU GPL v3 or later
Logged in as: %s
*****************************************************************\n"""

SSH_SERVER_NOT_MOUNTED_MSG = 'The filesystem is not mounted. Please contact '\
                             'the administrator.\n'\
                             'You have to type "exit" to leave'\

SSH_PUBLIC_KEY = \
    'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAAAgQCnuBWo39zhKg2z5hq7fEGTXpNJk+sAr6S3' \
    '21cw4nP5ZZS04c1RnUrBsBCAoo9Nw8VRb3MVT7vfWJxcJCXSfQfqItjEMSsqVSjB4THl2JX8' \
    'Qw8GjZANwbCPly+FzdGuA99b5iWJzJ3oK8mK2KK9J1fG8StHAJ+827mTIuovkQaryw== nicu'

SSH_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIICXwIBAAKBgQCnuBWo39zhKg2z5hq7fEGTXpNJk+sAr6S321cw4nP5ZZS04c1R
nUrBsBCAoo9Nw8VRb3MVT7vfWJxcJCXSfQfqItjEMSsqVSjB4THl2JX8Qw8GjZAN
wbCPly+FzdGuA99b5iWJzJ3oK8mK2KK9J1fG8StHAJ+827mTIuovkQarywIDAQAB
AoGBAISFQKAB2l4TQ2Z9D2xKnunZlZlShiIxpn4bkoYuuCI8MEbID9pH5VSrUC7D
w2VXpaZV4GHbcX/lXQ61BSmO31vJ2WZPRiPauSyHWSYWoog6KeZIDwe0Mkf0nhMq
vcYxMzQYGBcHNvdslhW0B79ph29CvY0AQbltostxSkWAmRt5AkEA3e+nJll4KbID
YOERDRoY3vFkhzoSntBUyeRcP5Z5WXHLBoz0uYMi6r1xsCCg1qhdo+DYK+wpZPjj
eCV0w9CALQJBAMF2IIElAHL5dFudgYdwzNlqGtvq1Q8FpJZ/VZcQ406pM01qJT3T
/4mkoUcXvVcaVv6Xwjyy2xYmywt+V5tU3tcCQQDPuuc7D/dXH5Xl8gPhvZGV61/q
6sJPADS8nBB0PEXtIIOl5/2QPlxKV3O4JXImOYUcRPJRekTsi8FtzbFTLy8pAkEA
lM9zg0NeDBJ8AXivSOpoeBhY3q7NAkgZ6TW7NX9lCX23G6Y5TUzD9DFxaQkGuHhn
UGCVpTECuxBOAOJHKxFmcwJBAJFtIvhYL5t/K1C5daS8ItlglSfaEWiyuIyBrddo
bAUHQ90eaPYpD9gYVxdd/DfnAUSVZbD0GT0igENkDqXDrDU=
-----END RSA PRIVATE KEY-----"""
