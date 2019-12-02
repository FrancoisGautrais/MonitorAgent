import os


class Conf:

    def __init__(self):
        self.workingdir=os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def savedir(name):
        return os.path.join(_conf.workingdir, "save", name)

_conf=None

if not _conf:
    _conf=Conf()

def conf():
    return