import platform
import os


class Globals:
    def __init__(self):
        self._os=platform.system()
        self._osRelease=platform.release()
        self._osVersion=platform.release()
        self._pythonVersion=platform.python_version()
        self._version=(0,0,0)
        self._port=443
        self._host="127.0.0.1"
        self._dir=os.path.dirname(os.path.realpath(__file__))
        self._conf=os.path.join(self._dir,"conf/")
        with open("version") as f:
            print(tuple(f.read().split(".")))


    @staticmethod
    def conf(subpath):
        return os.path.join(Globals.instance._conf, subpath)

    @staticmethod
    def isWindows():
        return Globals.instance._os.lower()=="windows"



print(hasattr(Globals, "instance"))
if not hasattr(Globals, "instance"):
    Globals.instance=Globals()
print(hasattr(Globals, "instance"))
print(Globals.instance.conf("test"))

def getInstance():
    return Globals.instance