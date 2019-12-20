import subprocess
import os
from agent.commandreturn import CommandReturn
from conf import Conf

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
        if Conf.isWindows():
            os.system(argsToString(cmd))
        else:
            pid=os.fork()
            if pid:
                os.waitpid(pid,0)
            else:
                os.execv(cmd[0], cmd)

        return  CommandReturn( 0)

import datetime

def timestamp_to_time(s):
    s%=24*3600
    h=int(s%3600)
    m=int( (s/60)%60)
    sec=int( (s/3600))
    micro=int( (s%1)*1000000)
    return datetime.time(h,m,sec,micro)

def time_to_timestamp(t):
    return t.hour*3600+t.minute*60+t.second+t.microsecond/1000000

