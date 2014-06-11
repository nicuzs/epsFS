import os
import threading
import signal
from subprocess import Popen, PIPE

from twisted.conch import recvline
from settings import ABSOLUTE_MOUNTPOINT_PATH, FILESYSTEM_SOURCE_ROOT, \
    SSH_SERVER_WELCOME_MSG, SSH_SERVER_NOT_MOUNTED_MSG, FILE_SYS_PATH
from data_processors import get_user_data


# def execute_as_logged_user(f):
#     def wrapper(*args):
#         os.seteuid(args[0].root_uid)
#         os.seteuid(args[0].user_data.get('uid'))
#         r = f(*args)
#         os.seteuid(args[0].root_uid)
#         return r
#     return wrapper


class FsepsSshProtocol(recvline.HistoricRecvLine):
    """
        The protocol will just place the user in a specific directory from
        the filesystem and execute standard bash commands.
    """
    fs_mount_state = True   # becomes true when the fs is mounted
    user_data = {}          # the info we store regarding the user
    # thread_mount = None     # thread responsible to mount the fs

    def __init__(self, user):
        self.user = user
        self.root_uid = os.getuid()  # this is usually 0

    def connectionMade(self):
        recvline.HistoricRecvLine.connectionMade(self)
        self.user_data = get_user_data(self.user.username)
        self.terminal.write(SSH_SERVER_WELCOME_MSG % self.user.username)
        self.terminal.nextLine()
        #mount the thing here
        self.mount_fs()
        self.show_prompt()

    # def chech_fs_mounted(self):
    #     srcout, srcerr = self.execute_bash_cmd('ls %s' % FILESYSTEM_SOURCE_ROOT)
    #     out, err = self.execute_bash_cmd('ls %s' % ABSOLUTE_MOUNTPOINT_PATH)
    #     if out != srcout or err != srcerr:
    #         self.terminal.write(SSH_SERVER_NOT_MOUNTED_MSG)
    #         self.terminal.nextLine()
    #         return
    #     self.fs_mount_state = True
    #     os.chdir(ABSOLUTE_MOUNTPOINT_PATH % self.user.username)

    def execute_bash_cmd(self, cmd):
        try:
            p = Popen('sudo -u %s %s' % (self.user.username, cmd),
                      shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            return p.communicate()
        except Exception as ex:
            print '[Bash cmd execution err:]' + str(ex)
            return None, None

    def show_prompt(self):
        stdout, stderr = self.execute_bash_cmd('date')
        fs_local_time = stdout.split(' ')[-2]

        if self.fs_mount_state:
            out, err = self.execute_bash_cmd('pwd')
        self.terminal.write('%s[%s] $ ' %
                            (out if self.fs_mount_state else '',
                             fs_local_time))

    def lineReceived(self, line):
        # os.seteuid(self.root_uid)
        # if self.user.username == 'nicu':
        #     os.seteuid(1000)
        # elif self.user.username == 'tim':
        #     os.seteuid(1001)

        line = line.strip()
        print 'User [%s] requested:>>%s<<' % (self.user.username, line)
        if line:
            if line.startswith('exit'):
                self.exit()
                return
            elif line.startswith('cd') and self.fs_mount_state:
                self.chdir(line)
            elif self.fs_mount_state:
                self.run_cmd(line)
            else:
                self.mount_fs()
            self.show_prompt()

    def chdir(self, line):
        try:
            cmd_args = line.split(' ')
            if len(cmd_args) >= 2:
                os.chdir(cmd_args[1])
        except OSError as oserr:
            self.terminal.write(oserr.strerror + '\n')
            self.terminal.nextLine()

    def mount_fs(self):
        """
            Mounting the filesystem for a specific user !! never as root
        """
        self.fs_mount_state = self.execute_bash_cmd_nowait(
            'sudo -u %s ./activate.sh' % self.user.username)

    def execute_bash_cmd_nowait(self, cmd='sudo -u %s ./activate.sh'):
        # used to mount the fs
        try:
            Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            return True
        except Exception as ex:
            print '[Bash cmd execution err:]' + str(ex)
            return False

    def run_cmd(self, line):
        stdout, stderr = self.execute_bash_cmd(line)
        self.terminal.write(stdout if stdout else stderr)
        self.terminal.nextLine()

    def exit(self):
        f = open('%s/unmount/%s_mount.pid'
                 % (FILE_SYS_PATH, self.user.username),
                 'r')
        pid = int(f.readline().strip())
        if pid:
            try:
                os.kill(pid, signal.SIGINT)
            except OSError:
                print 'oserror---->'
        else:
            # unable to unmount the thing, no problem
            pass
        self.terminal.write('Bye!')
        self.terminal.nextLine()
        self.terminal.loseConnection()
        self.terminal.reset()
        # TODO unmount the FS
