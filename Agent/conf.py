import platform
import os
import socket
import uuid

class Conf:

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
        return os.path.join(Conf.instance._conf, subpath)

    @staticmethod
    def is_agent(): return True

    @staticmethod
    def is_server(): return False

    @staticmethod
    def isWindows():
        return Conf.instance._os.lower()=="windows"

    @staticmethod
    def getAllversionInformation():
        return {
            "os": Conf.instance._os,
            "osRelease": Conf.instance._osRelease,
            "osVersion": Conf.instance._osVersion,
            "pythonVersion": Conf.instance._pythonVersion,
            "version": Conf.instance._version,
            "name": Conf.instance._name,
            "uuid": Conf.instance._uuid
        }

    @staticmethod
    def data(key, val=None):
        if val!=None:
            Conf.instance._data[key]=val
        elif not key in Conf.instance._data:
            return None
        return Conf.instance._data[key]

    @staticmethod
    def hasData(key):
        return key in Conf.instance._data


if not hasattr(Conf, "instance"):
    Conf.instance=Conf()
    exec(open("./conf/config.py").read())


def getInstance():
    return Conf.instance