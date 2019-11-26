import os
from agent import  errors
from agent.commandreturn import CommandReturn
from agent.shell import Shell
from conf import Globals
from utils import execSystem


def cmd_env(shell : Shell, args):
    out=""
    if len(args)==0:
        for k in shell._env:
            out+=k+" = '"+shell._env[k]+"'\n"
        out=out[:-1]
    elif len(args)==1:
        if not args[0] in shell._env:
            return CommandReturn(errors.BAD_PARAMETER, "'"+args[0]+"' is not defined")
        out=shell._env[args[0]]
    elif len(args)==3 and args[1]=="=":
        shell._env[args[0]]=args[2]
    else:
        print("Error ", len(args), '"'+args[1]+'"', "'")
    return CommandReturn(errors.OK, out)