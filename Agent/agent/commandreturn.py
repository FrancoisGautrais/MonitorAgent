class CommandReturn:
    def __init__(self, code, error, out=None):
        self.code=code
        self.error=error
        self.out=out