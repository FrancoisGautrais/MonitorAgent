class CommandReturn:
    def __init__(self, code, out=""):
        self.code=code
        self.out=out if out != None else ""