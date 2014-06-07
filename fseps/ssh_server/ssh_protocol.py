from twisted.conch import recvline
from subprocess import Popen, PIPE
from settings import FILESYSTEM_ACCESS_ROOT
from os import chdir


class FsepsSshProtocol(recvline.HistoricRecvLine):
    """
        The protocol will just place the user in a specific directory from
        the filesystem and execute standard bash commands.
    """
    def __init__(self, user):
        self.user = user

    def connectionMade(self):
        recvline.HistoricRecvLine.connectionMade(self)
        self.terminal.write('*****************WELCOME********************\n'
                            '   Welcome to your private space via ssh!!\n'
                            '   Logged in as: %s\n'
                            '************************************************\n'
                            % self.user.username)
        self.terminal.nextLine()
        # TODO make sure that the filesystem is mounted, or close the connection
        chdir(FILESYSTEM_ACCESS_ROOT)
        self.show_prompt()

    def execute_bash_cmd(self, cmd):
        try:
            p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            return p.communicate()
        except Exception as ex:
            print '[Bash cmd execution err:]' + str(ex)
            return None, None

    def show_prompt(self):
        stdout, stderr = self.execute_bash_cmd('date')
        fs_local_time = stdout.split(' ')[-2]
        stdout, stderr = self.execute_bash_cmd('pwd')

        self.terminal.write('%s[%s] $ ' % (stdout, fs_local_time))

    def lineReceived(self, line):
        line = line.strip()
        if line:
            if line.startswith('exit'):
                self.terminal.write('Bye!')
                self.terminal.nextLine()
                self.terminal.loseConnection()
                return
            elif line.startswith('cd'):
                try:
                    cmd_args = line.split(' ')
                    if len(cmd_args) >= 2:
                        chdir(cmd_args[1])
                except OSError as oserr:
                    self.terminal.write(oserr.strerror + '\n')
                    self.terminal.nextLine()
            else:
                stdout, stderr = self.execute_bash_cmd(line)
                self.terminal.write(stdout if stdout else stderr)
                self.terminal.nextLine()
            self.show_prompt()


            # cmdAndArgs = line.split()
            # cmd = cmdAndArgs[0]
            # args = cmdAndArgs[1:]
            # func = self.getCommandFunc(cmd)
            # if func:
            #     try:
            #         func(*args)
            #     except Exception, e:
            #         self.terminal.write("Error: %s" % e)
            #         self.terminal.nextLine()
            # else:
            #     self.terminal.write("No such command.")
            #     self.terminal.nextLine()
            # self.show_prompt()

    # def do_help(self):
    #     publicMethods = filter(
    #         lambda funcname: funcname.startswith('do_'), dir(self))
    #     commands = [cmd.replace('do_', '', 1) for cmd in publicMethods]
    #     self.terminal.write("Commands: " + " ".join(commands))
    #     self.terminal.nextLine()
    #
    # def do_echo(self, *args):
    #     self.terminal.write(" ".join(args))
    #     self.terminal.nextLine()
    #
    # def do_whoami(self):
    #     self.terminal.write(self.user.username)
    #     self.terminal.nextLine()
    #
    # def do_quit(self):
    #     self.terminal.write("Thanks for playing!")
    #     self.terminal.nextLine()
    #     self.terminal.loseConnection()
    #
    # def do_clear(self):
    #     self.terminal.reset()
