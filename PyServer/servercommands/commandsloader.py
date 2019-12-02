import os
import inspect
import sys
from importlib import import_module
from inspect import getmembers, isfunction
import errors

class CommandReturn:
    def __init__(self, code, out=""):
        self.code=code
        self.out=out if out != None else ""
        self.cmd=-1

    def setid(self, id):
        self.cmd=id

    def json(self):
        return {
            "code" : self.code,
            "stdout": self.out,
            "id": self.cmd
        }

class _CommandsLoader:

    def __init__(self):
        self.commands={}
        self.load()


    def load(self):
        filename = inspect.getframeinfo(inspect.currentframe()).filename
        path = os.path.dirname(os.path.abspath(filename))
        path += "/commands/"
        for x in os.listdir(path):
            if x[0]!="_" and (x[-3:].lower()==".py" or x[-4:].lower()==".pyc"):
                imported_module = import_module("servercommands.commands."+x.split(".")[0])

                functions_list = [o for o in getmembers(imported_module) if isfunction(o[1])]
                for k in functions_list:
                    if k[0].startswith("cmd_"):
                        self.commands[k[0][4:]]=k[1]

    def call(self, server, name, args):
        x=None
        if not name in self.commands:
            sys.stderr.write("Command '"+str(name)+"' not found\n")
        try:
            x=self.commands[name](server, args)
            return x
        except KeyError as err:
            return CommandReturn(errors.COMMAND_NOT_FOUND, str(name)+" : commande inconnue\n")
        except ValueError as err:
            return CommandReturn(errors.BAD_PARAMETER, str(name)+" : "+str(err))
_instance=None

def call(shell, name, args=[]):
    global _instance
    if _instance==None: _instance=_CommandsLoader()
    return _instance.call(shell, name, args)
