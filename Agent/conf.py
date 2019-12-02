import platform
import os
import socket
import uuid

class Globals:

    def __init__(self):
        self._os=platform.system()
        self._osRelease=platform.release()
        self._osVersion=platform.version()
        self._pythonVersion=platform.python_version()
        self._version=(0,0,0)
        self._port=443
        self._host="127.0.0.1"
        self._data={}
        self._dir=os.path.dirname(os.path.realpath(__file__))
        self._conf=os.path.join(self._dir,"conf/")
        self._name=socket.gethostname()
        self._uuid=str(uuid.getnode())
        with open("version") as f:
            self._version=tuple(f.read().split("."))


    @staticmethod
    def conf(subpath):
        return os.path.join(Globals.instance._conf, subpath)

    @staticmethod
    def isWindows():
        return Globals.instance._os.lower()=="windows"

    @staticmethod
    def getAllversionInformation():
        return {
            "os": Globals.instance._os,
            "osRelease": Globals.instance._osRelease,
            "osVersion": Globals.instance._osVersion,
            "pythonVersion": Globals.instance._pythonVersion,
            "version": Globals.instance._version,
            "name": Globals.instance._name,
            "uuid": Globals.instance._uuid
        }

    @staticmethod
    def data(key, val=None):
        if val!=None:
            Globals.instance._data[key]=val
        elif not key in Globals.instance._data:
            return None
        return Globals.instance._data[key]

    @staticmethod
    def hasData(key):
        return key in Globals.instance._data


if not hasattr(Globals, "instance"):
    Globals.instance=Globals()
    exec(open("./conf/config.py").read())


def getInstance():
    return Globals.instance