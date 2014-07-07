import os
from subprocess import Popen, PIPE

from settings import EPSFS_CONFIG_USR, EPSFS_CONFIG_GRP, EPSFS_SSH_MOCK


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


# def get_connected_ssh_users():
#     ssh_users = {}
#     with open(EPSFS_SSH_MOCK) as fp:
#         for line in fp:
#             data = line.strip().split(';')
#             ssh_users[data[0]] = {
#                 'protocol': data[1],
#                 'ip': data[2],
#             }
#     return ssh_users


def get_connected_ssh_users():
    ssh_users = {}
    #'sudo netstat -atpn|grep ssh'
    out, err = Popen(
        'sudo netstat -atpn|grep ssh | '
        'awk -F " " \'{ print $5 ";" $7 ";" $8 }\'',
        shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()
    if out:
        for line in out.splitlines():
            line_items = line.split(';')
            if len(line_items) == 3 and line_items[2]:
                ssh_users[line_items[2]] = {
                    'protocol': 'ssh' if 'ssh' in line_items[1] else '',
                    'ip': line_items[0].split(':')[0]
                }
    return ssh_users
