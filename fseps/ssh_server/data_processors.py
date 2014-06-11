import os

from settings import USER_STORAGE_LOCATION


def get_user_data(uname=None, uid=None):
    if not uname and not uid:
        raise Exception("At least one parameter should be provided!")
    with open(USER_STORAGE_LOCATION) as fp:
        for line in fp:
            user_data = line.strip().split(';')
            if len(user_data) and (user_data[0] == uid
                                   or user_data[1] == uname):
                return {
                    'uid': int(user_data[0]),
                    'uname': user_data[1],
                    'groups': []}
        return {}
