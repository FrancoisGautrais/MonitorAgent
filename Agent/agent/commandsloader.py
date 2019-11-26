import os
import inspect
from conf import Globals
from importlib import import_module
from inspect import getmembers, isfunction





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
                print("----------------------------", imported_module.__dict__)

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
        print(self.commands)
        x=self.commands[name](shell, args)
        if not x: return 0
        return x

_instance=_CommandsLoader()

def call(shell, name, args=[]):
    return _instance.call(shell, name, args)