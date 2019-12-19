import os
from agent import  errors
from agent.commandreturn import CommandReturn
from agent.shell import Shell
from conf import Conf
from utils import execSystem

def absjoin(base, after):
    return os.path.abspath(os.path.join(base, after))

def cmd_cd(shell : Shell, args):
    np=absjoin(shell.getPwd(), args[0])
    if os.path.isdir(np):
        if Conf.isWindows() and np[-1]==":": np+="\\"
        shell.setPwd(np)
        return CommandReturn(errors.OK)
    elif os.path.exists(np):
        return CommandReturn(errors.FILE_NOT_FOUND, "'"+args[0]+"' not a directory")
    else:
        return CommandReturn(errors.FILE_NOT_FOUND, "'"+args[0]+"' no file or directory")

def cmd_pwd(shell: Shell, args):
    return CommandReturn(errors.OK, shell.getPwd())

def cmd_ls(shell: Shell, args):
    dir=shell.getPwd()

    if len(args)>0: dir=absjoin(dir, args[0])

    if os.path.isdir(dir):
        return CommandReturn(errors.OK, "\n".join(os.listdir(dir)))
    elif os.path.exists(dir):
        return CommandReturn(errors.FILE_NOT_FOUND,  "Not a directory")
    else:
        return CommandReturn(errors.FILE_NOT_FOUND,  "No such file or directory")

def cmd_rm(shell: Shell, args):
    for w in args:
        file = absjoin(os.path.abspath(shell.getPwd()), w)
        if os.path.isfile(file):
            os.remove(w)
        elif os.path.isdir(file):
            return CommandReturn(errors.FILE_NOT_FOUND, "'"+w+"' is not a file'" )
        else:
            return CommandReturn(errors.FILE_NOT_FOUND,  "'"+w+"' no such file or directory")

def cmd_mkdir(shell : Shell, args):
    if isinstance(args, str): args=[args]
    for x in args:
        os.mkdir(x)
    return CommandReturn(errors.OK, "")


def cmd_cp(shell: Shell, args):
    if Conf.isWindows():
        return execSystem(["copy"] + args)
    else:
        return execSystem(["cp"] + args)


def cmd_mv(shell: Shell, args):
    if Conf.isWindows():
        return execSystem(["move"] + args)
    else:
        return execSystem(["mv"] + args)

