from .commandsloader import call


class Command:

    def __init__(self, d):
        print(d)
        self.doBefore=None
        self.doAfter=None
        self.id=d["id"]
        self.cmd=d["cmd"]
        self.args=d["args"] if hasattr(d, "args") else []

        if hasattr(d, "doBefore"):
            self.doBefore=Command(d["doBefore"])
        if hasattr(d, "doAfter"):
            self.doBefore=Command(d["doAfter"])

    def start(self):
        out={}
        print(self.id)
        if self.doBefore:
            out[self.doBefore.id]=self.doBefore.start()
        out[self.id]=call(self.cmd, self.args)
        if self.doAfter:
            out[self.doAfter.id]=self.doAfter.start()

        return out
