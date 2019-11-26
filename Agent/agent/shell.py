import os
from conf import Globals
from utils import Stack
from .command import Command

class Shell:

    def __init__(self, agent, parent=None):
        self._env={}
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

    def getPwd(self):
        return self._dir


    def setPwd(self, d):
        self._dir=d

