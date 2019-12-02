import subprocess
import os
from agent.commandreturn import CommandReturn
from conf import Globals

class Stack:

    def __init__(self):
        self._data=[]

    def push(self, val):
        self._data.append(val)
        return val

    def pop(self):
        if self.isEmpty(): return None
        return self._data.pop()

    def peak(self):
        if self.isEmpty(): return None
        return self._data[-1]

    def isEmpty(self):
        return len(self._data)==0

def argsToString(args):
    out=""
    for arg in args:
        putGuill=""
        for x in " \t\n":
            if x in arg:
                putGuill='"'
                break
        out+=putGuill+arg+putGuill+" "
    return out[:-1]

def execSystem(cmd, pipe=True,input=None):
    if pipe:
        x=subprocess.run(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        return CommandReturn(x.returncode, x.stdout)
    else:
        #x = subprocess.Popen(cmd)
        print(cmd)
        if Globals.isWindows():
            os.system(argsToString(cmd))
        else:
            pid=os.fork()
            if pid:
                os.waitpid(pid,0)
            else:
                os.execv(cmd[0], cmd)

        return  CommandReturn( 0)