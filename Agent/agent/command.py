from .commandsloader import call
import uuid




class Lexer:

    def __init__(self, text):
        self._text=text.rstrip("\n")
        self._i=0
        self._current=""

    def _c(self):
        return self._text[self._i]

    def _nc(self):
        if self._i+1>=len(self._text): return None
        self._i+=1

        return self._c()

    def _isSep(self, c=None):
        if c==None: c=self._c()
        return c in " \t\r\n"

    def hasNext(self):
        return self._i!=len(self._text)-1

    def peak(self): return self._current

    def next(self):
        self._current=""
        if not self.hasNext(): return None
        while self._isSep(): self._nc()

        if self._c()=="\'" or self._c()=='"':
            x=self._c()
            self._current=""
            self._nc()
            while self.hasNext() and (self._c()!=x or self._current[-1]=="\\"):
                self._current+=self._c()
                self._nc()
            return self._current

        while True:
            if (not self.hasNext()) or self._isSep():
                return self._current if (self.hasNext()) else self._current+self._c()
            self._current+=self._c()
            self._nc()

class Command:

    def __init__(self, d):
        print(d)
        self.doBefore=None
        self.doAfter=None
        self.id=d["id"]
        self.cmd=d["cmd"]
        self.args=d["args"] if ("args" in d) else []

        if hasattr(d, "doBefore"):
            self.doBefore=Command(d["doBefore"])
        if hasattr(d, "doAfter"):
            self.doBefore=Command(d["doAfter"])

    def start(self, shell):
        """
        out={}
        if self.doBefore:
            out[self.doBefore.id]=self.doBefore.start()
        out[self.id]=call(shell, self.cmd, self.args)
        if self.doAfter:
            out[self.doAfter.id]=self.doAfter.start()
        """
        return call(shell, self.cmd, self.args)

    @staticmethod
    def fromText(txt):
        l=Lexer(txt)
        cmd=l.next()
        args=[]
        while l.next()!=None and l.peak()!="":
            args.append(l.peak().rstrip())

        return Command({
            "id": uuid.uuid4(),
            "cmd": cmd,
            "args": args
        })

