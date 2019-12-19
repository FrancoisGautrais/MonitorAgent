import os
import platform
import socket
import uuid

class Conf:

    def __init__(self):
        self.workingdir=os.path.dirname(os.path.realpath(__file__))
        self._os = platform.system()
        self._os_release = platform.release()
        self._os_version = platform.version()
        self._python_version = platform.python_version()
        self._version = (0, 0, 0)
        self._port = 443
        self._host = "127.0.0.1"
        self._data = {}
        self._dir = os.path.dirname(os.path.realpath(__file__))
        self._conf = os.path.join(self._dir, "conf/")
        self._name = socket.gethostname()
        self._uuid = str(uuid.getnode())
        with open("version") as f:
            self._version = tuple(f.read().split("."))

    @staticmethod
    def savedir(name):
        return os.path.join(Conf._conf.workingdir, "save", name)

    @staticmethod
    def is_windows():
        return Conf._conf._os.lower()=="windows"


    @staticmethod
    def is_agent(): return False

    @staticmethod
    def is_server(): return True

Conf._conf=Conf._conf=Conf()

def conf():
    return