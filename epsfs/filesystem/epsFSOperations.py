import os
import stat
import time
import errno
import datetime

from fuse import FuseOSError, Operations, fuse_get_context
from settings import EPSFS_PERMISSIONS_FILE_NAME
from sys_utils import load_users, load_groups


class EpsFSOperations(Operations):
    def __init__(self, root):
        self.root = root
        self.users = load_users()
        self.groups = load_groups()
        # self.processed = False
        #self.processed_files = [] this will help you with concurrent users

        for i, v in self.users.items():
            print i, '--->', v
        print type(self.groups)
        for i, v in self.groups.items():
            print i, '--->', v

    # Utils
    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    def get_group_id(self, group_name):

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

    def get_inherited_permissions(self):
        pass


    def create_perms_file(self, full_current_path):
        """
        The file mode is 700 but it doesn't actually matter
        (except outside the fs)
        """
        return os.open(full_current_path + '/' + EPSFS_PERMISSIONS_FILE_NAME,
                       os.O_WRONLY | os.O_CREAT,
                       stat.S_IRWXU)

    # System calls
    def access(self, path, mode):
        full_path = self._full_path(path)
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
        print '-->', self.get_eps_context()
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        dirents = [x for x in dirents if x != EPSFS_PERMISSIONS_FILE_NAME]
        for r in dirents:
            yield r

    def readlink(self, path):
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        full_path = self._full_path(path)
        return_val = os.mkdir(full_path, mode)

        self.create_perms_file(full_path)
        return return_val

    # File methods
    def open(self, path, flags):
        dir_path, filename = os.path.split(path)
        if filename == EPSFS_PERMISSIONS_FILE_NAME:
            raise FuseOSError(errno.ENOENT)
        upper_bound = datetime.time(18, 0, 0)
        lower_bound = datetime.time(9, 0, 0)
        now = datetime.datetime.now().time()
        # if now > upper_bound or now < lower_bound:
        # raise FuseOSError(errno.EACCES, "adfsdfsdfas")
        full_path = self._full_path(path)
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
        print 'read'
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        print 'write'
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
