import os
import stat
import time
import errno
import datetime
import re

from fuse import FuseOSError, Operations, fuse_get_context
from settings import EPSFS_PERMISSIONS_FILE_NAME, EPSFS_AND, EPSFS_OR
from sys_utils import load_users, load_groups, get_connected_ssh_users
from models import AccesRule

EPSFS_OPERANDS = (EPSFS_AND, EPSFS_OR)


class EpsFSOperations(Operations):
    def __init__(self, root):
        self.root = root
        self.users = load_users()
        self.groups = load_groups()
        # self.processed = False
        #self.processed_files = [] this will help you with concurrent users

        for i, v in self.users.items():
            print i, '--->', v
        for i, v in self.groups.items():
            print i, '--->', v

    # Utils
    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    def get_group_id(self, group_name):
        """
        Return the matching uid for the required group_name or None
        """
        group_ids = [g.get('gid') for g in self.groups.values()
                     if g.get('gname') == group_name]
        return group_ids[0] if group_ids else None

    def get_eps_context(self):
        context_data = list(fuse_get_context())

        group_ids = [self.get_group_id(gname) for gname in
                     self.users.get(context_data[0], {}).get('groups')]
        group_ids.sort()
        context_data[1] = group_ids
        return tuple(context_data)

    def check_ancestor(self, group_id, required_id):
        """
        Return true if required_id is an ancestor of group_id
        """
        crt_gid = group_id
        while True:
            crt_group = self.groups.get(crt_gid)
            if not crt_group or not crt_group.get('parent'):
            # didn't found the required_id and the current pos is the root of
            # the branch
                return False
            parent_id = self.get_group_id(crt_group.get('parent'))
            if parent_id == required_id:
            # required_id is an ancestor of group_id stop the execution
                return True
            crt_gid = parent_id

    def create_perms_file(self, full_current_path):
        """
        The file mode is 700 but it doesn't actually matter
        (except outside the fs)
        """
        return os.open(full_current_path + '/' + EPSFS_PERMISSIONS_FILE_NAME,
                       os.O_WRONLY | os.O_CREAT,
                       stat.S_IRWXU)

    def process_perms_file(self, perms_path):
        with open(perms_path + '/' + EPSFS_PERMISSIONS_FILE_NAME) as fp:
            crt_dir_rules = {}
            i = 0
            for line in fp:
                if not line.strip():
                    continue
                line_group = line.strip().split(':')
                if len(line_group) != 2:
                    raise IOError("The perms file doesn't follow the protocol")
                file_name = line_group[0]
                values = [s.strip() for s in re.split('|'.join(EPSFS_OPERANDS),
                                                      line_group[1])]

                ar = AccesRule(
                    owner_type='user' if i == 0 else ('group' if i == 1
                                                      else 'others'),
                    owner_id=int(values[0].strip())
                        if values[0].strip() else None,
                    protocol=values[1] if values[1].lower() == 'ssh' else True,
                    ip=values[2] if values[2] else True,
                    date=values[3] if values[3] else True,
                    time_interval=values[4] if values[4] else True,
                )
                raw_perms = values[-1]
                #Establish the permissions
                temp = [False, False, False]
                if len(raw_perms) == 3:
                    temp[0] = True if raw_perms[0] == 'r' else False
                    temp[1] = True if raw_perms[1] == 'w' else False
                    temp[2] = True if raw_perms[2] == 'x' else False
                ar.effective_rights = temp

                # VERY IMPORTANT: increment the crt_position
                i = i+1 if i in [0, 1] else 0

                operators = re.findall('|'.join(EPSFS_OPERANDS), line_group[1])
                if len(operators) > 2:
                    del(operators[0])
                    del(operators[-1])
                ar.operators = operators

                if not crt_dir_rules.get(file_name):
                    crt_dir_rules[file_name] = []
                crt_dir_rules[file_name].append(ar)

            return crt_dir_rules

    def get_user_access_for_file(self, epsfs_context, full_file_path):
        """
        Open the corresponding ,epsfs file and retrieve the acces rights
        returns something like rwx or r-x ...
        """
        request = {
            'uid': epsfs_context[0],
            'gids': epsfs_context[1],
            'pid': epsfs_context[2]}
        dir_path, filename = os.path.split(full_file_path)
        if not filename:
            return [True, True, True]  #all users are allowed to access the root
        crt_dir_rules = self.process_perms_file(dir_path)
        for k, v in crt_dir_rules.items():
            for j in v:
                print k, '===', j
        print '\n you are here: ', dir_path, '->', filename, '\n'

        return_perms = [False, False, False]
        file_attached_perms = crt_dir_rules.get(filename)
        if not file_attached_perms:
            print 'No access rules found on disk'
            return return_perms

        for access_rule in file_attached_perms:
            if access_rule.owner_type == 'user':
                if access_rule.owner_id != request['uid']:
                    # the user restrictions do not apply for this request
                    continue
                # more stuff here
                return access_rule.effective_rights
            elif access_rule.owner_type == 'group':
                gid_match = None
                # maby check straight forward if it matches ??
                if access_rule.owner_id in request.get('gids'):
                    gid_match = access_rule.owner_id
                else:
                    for gid in request.get('gids'):
                        if self.check_ancestor(gid, access_rule.owner_id):
                            gid_match = gid
                            break
                if not gid_match:
                    # the group restrictions do not apply for this request
                    continue
                return access_rule.effective_rights
            elif access_rule.owner_type == 'others':
                #check ssh and ip here

                if access_rule.protocol:
                    print 'sssshsshhshshs match here '
                    crt_user = self.users.get(request['uid'], {})
                    ssh_users = get_connected_ssh_users()

                    print crt_user
                    print 'request', ssh_users.get(crt_user.get('uname'),{}).get('protocol')
                    print 'fileattach', access_rule.protocol
                    SSH_STATUS = True if ssh_users.get(
                        crt_user.get('uname'),
                        {}).get('protocol') == access_rule.protocol else False
                    print 'ssh->', SSH_STATUS


                return access_rule.effective_rights
        # for i in asdf:
        #     perms = [x | y for (x, y) in zip(perms, i.effective_rights)]
        return return_perms

    # System calls
    def access(self, path, mode):
        # same as open for file aka read
        full_path = self._full_path(path)
        computed_perms = self.get_user_access_for_file(self.get_eps_context(),
                                                       full_path)
        if not computed_perms[0]:
            raise FuseOSError(errno.EACCES)

        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)


    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                                                        'st_gid', 'st_mode',
                                                        'st_mtime', 'st_nlink',
                                                        'st_size', 'st_uid',
                                                        'st_rdev'))

    def readdir(self, path, fh):
        # aka execute
        print '-->', self.get_eps_context()
        full_path = self._full_path(path)
        computed_perms = self.get_user_access_for_file(self.get_eps_context(),
                                                       full_path)
        if not computed_perms[2]:
            raise FuseOSError(errno.EACCES)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        dirents = [x for x in dirents if x != EPSFS_PERMISSIONS_FILE_NAME]
        for r in dirents:
            yield r

    def readlink(self, path):
        print "readlink"
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        print "rmdir"
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        full_path = self._full_path(path)
        return_val = os.mkdir(full_path, mode)

        self.create_perms_file(full_path)
        return return_val

    # File methods
    def open(self, path, flags):
        full_path = self._full_path(path)
        dir_path, filename = os.path.split(path)
        if filename == EPSFS_PERMISSIONS_FILE_NAME:
            raise FuseOSError(errno.ENOENT)

        upper_bound = datetime.time(18, 0, 0)
        lower_bound = datetime.time(9, 0, 0)
        now = datetime.datetime.now().time()
        # if now > upper_bound or now < lower_bound:
        # raise FuseOSError(errno.EACCES)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        uid, gid, pid = self.get_eps_context()
        print mode, "-->", fi, type(mode)
        dir_path, filename = os.path.split(path)
        if filename == EPSFS_PERMISSIONS_FILE_NAME:
            raise FuseOSError(errno.ENOENT)
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        full_path = self._full_path(path)
        computed_perms = self.get_user_access_for_file(self.get_eps_context(),
                                                       full_path)
        if not computed_perms[0]:
            raise FuseOSError(errno.EACCES)

        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        full_path = self._full_path(path)
        computed_perms = self.get_user_access_for_file(self.get_eps_context(),
                                                       full_path)
        if not computed_perms[1]:
            raise FuseOSError(errno.EACCES)
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        return self.flush(path, fh)
