#!/bin/bash
# activate the env. and mount the filesystem
# this will be runned only by users forced by the root
# using sudo -u <username> activate.sh

. ../../ve/bin/activate
python mount_fs.py
