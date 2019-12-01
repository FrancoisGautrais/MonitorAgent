

class CommandReturn:
    def __init__(self, code, out=""):
        self.code=code
        self.out=out if out != None else ""
        self.cmd=-1

    def setid(self, id):
        self.cmd=id

    def toJson(self):
        return {
            "code" : self.code,
            "stdout": self.out,
            "id": self.cmd
        }