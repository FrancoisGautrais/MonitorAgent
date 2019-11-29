import os
from conf import Globals
from utils import Stack
from .command import Command

class Shell:

    def __init__(self, agent, parent=None):
        self._env={ "PATH" : os.environ["PATH"] }
        self._agent=agent
        self._parent=parent
        self._dir="C:\\" if Globals.isWindows() else "/"
        self._history=[]

    def getAgent(self):
        return self._agent

    def getParent(self):
        return self._parent

    def execCommand(self, cmd):
        return Command(cmd).start(self)

    def execCommandFromLine(self, line):
        return Command.fromText(line).start(self)

    def getPwd(self):
        return self._dir

    def findInPath(self, d):
        if not "PATH" in self._env: return ""
        if not Globals.isWindows():
            pp.replace(":", ";")
        pp=self._env["PATH"].split(";")
        for curr in pp:
            x=os.path.abspath(os.path.join( curr, d))
            if os.path.isfile(x):
                return x
            if Globals.isWindows() and os.path.isfile(x+".exe"):
                return x+".exe"
        return ""

    def setPwd(self, d):
        self._dir=d

