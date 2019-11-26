import os
from agent import  errors
from agent.commandreturn import CommandReturn
from agent.shell import  Shell

def cmd_cd(shell : Shell, args):
    np=os.path.join(shell.getPwd(), args[0])
    if os.path.isdir(np):
        shell.setPwd(np)
        return CommandReturn(errors.OK, "OK")
    elif os.path.exists(np):
        return CommandReturn(errors.BAD_PARAMETER, "Not a directory")
    else:
        return CommandReturn(errors.BAD_PARAMETER, "Not exists")

def cmd_pwd(shell: Shell, args):
    return CommandReturn(errors.OK, "OK", shell.getPwd())

def cmd_ls(shell: Shell, args):
    np=shell.getPwd()
    if len(args)>0: dir=os.path.join(np, args[0])

    if os.path.isdir(np):
        shell.setPwd(np)
        return CommandReturn(errors.OK, "OK", os.listdir(np))
    elif os.path.exists(np):
        return CommandReturn(errors.BAD_PARAMETER, "Not a directory")
    else:
        return CommandReturn(errors.BAD_PARAMETER, "Not exists")
