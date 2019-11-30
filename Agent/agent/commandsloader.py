import os
import inspect
import sys

from agent import errors
from conf import Globals
from importlib import import_module
from inspect import getmembers, isfunction

from .commandreturn import CommandReturn



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
                """
                attribute = getattr(imported_module, "load_commands")
                arr = attribute()
                for tu in arr:
                    cmd, fct = tu
                    self.commands[cmd]=fct

                """

    def call(self, shell, name, args):
        x=None
        if not name in self.commands:
            sys.stderr.write("Command '"+str(name)+"' not found\n")
        #x = self.commands[name](shell, args)
        try:
            x=self.commands[name](shell, args)
            return x
        except KeyError as err:
            return CommandReturn(errors.COMMAND_NOT_FOUND, str(name)+" : "+str(err)+"\n")

_instance=None

def call(shell, name, args=[]):
    global _instance
    if _instance==None: _instance=_CommandsLoader()
    return _instance.call(shell, name, args)
