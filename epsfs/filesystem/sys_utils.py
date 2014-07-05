import os

from settings import EPSFS_CONFIG_USR, EPSFS_CONFIG_GRP


def get_user_data(uname=None, uid=None):
    if not uname and not uid:
        raise Exception("At least one parameter should be provided!")
    with open(EPSFS_CONFIG_USR) as fp:
        for line in fp:
            user_data = line.strip().split(';')
            if len(user_data) and (int(user_data[0]) == int(uid)
                                   or user_data[1] == uname):
                return {
                    'uid': int(user_data[0]),
                    'uname': user_data[1],
                    'groups': user_data[2].split(',')
                }
        return None


def load_users():
    users = {}
    with open(EPSFS_CONFIG_USR) as fp:
        for line in fp:
            user_data = line.strip().split(';')
            users[int(user_data[0])] = {
                'uid': int(user_data[0]),
                'uname': user_data[1],
                'groups': user_data[2].split(',')
            }
    return users


def load_groups():
    groups = {}
    with open(EPSFS_CONFIG_GRP) as fp:
        for line in fp:
            user_data = line.strip().split(';')
            groups[int(user_data[0])] = {
                'gid': int(user_data[0]),
                'gname': user_data[1],
                'parent': user_data[2] if user_data[2] != 'None' else None
            }
    return groups


def get_groups(gname):
    pass


def get_connected_ssh_users():
    pass

