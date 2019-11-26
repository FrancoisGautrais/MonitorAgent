import os
import inspect
from conf import Globals
from importlib import import_module
from inspect import getmembers, isfunction
from utils import execSystem
from .commandreturn import CommandReturn
from agent import errors




class _CommandsLoader:

    def __init__(self):
        self.commands={}
        self.load()


    def load(self):
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(filename))
        if Globals.isWindows():
            path += "\\commands\\"
        else:
            path += "/commands/"
        for x in os.listdir(path):
            file=os.path.join(path, x)
            if x[0]!="_" and (x[-3:].lower()==".py" or x[-4:].lower()==".pyc"):
                imported_module = import_module("agent.commands."+x.split(".")[0])

                functions_list = [o for o in getmembers(imported_module) if isfunction(o[1])]
                for k in functions_list:
                    if k[0].startswith("cmd_"):
                        self.commands[k[0][4:]]=k[1]

    def call(self, shell, name, args):
        try:
            x=self.commands[name](shell, args)
            return x
        except:
            pass
        exe=shell.findInPath(name)
        if len(exe)>0:
            return execSystem([exe]+args, False)
        return CommandReturn(errors.BAD_PARAMETER, "'"+name+"' commande introuvable")


_instance=None

def init():
    global _instance
    _instance=_CommandsLoader()

def call(shell, name, args=[]):
    global _instance
    if _instance==None: init()
    return _instance.call(shell, name, args)
