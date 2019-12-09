import uuid
import json
from httpserver.utils import Callback
from servercommands.commandsloader import call, CommandReturn
class Lexer:

    def __init__(self, text):
        self._text=text.rstrip("\n")
        self._i=0
        self._current=""

    def _c(self):
        if self._i>= len(self._text): return "\0"
        return self._text[self._i]

    def _nc(self):
        if self._i+1>=len(self._text): return None
        self._i+=1

        return self._c()

    def _is_sep(self, c=None):
        if c==None:
            c=self._c()
        return c in " \t\r\n"

    def has_next(self):
        return self._i!=len(self._text)-1 and len(self._text)>0

    def peak(self): return self._current

    def next(self):
        self._current=""
        if not self.has_next(): return None
        while self._is_sep(): self._nc()

        if self._c()=="\'" or self._c()=='"':
            x=self._c()
            self._current=""
            self._nc()
            while self.has_next() and (self._c()!=x or self._current[-1]=="\\"):
                self._current+=self._c()
                self._nc()
            return self._current

        while True:
            if (not self.has_next()) or self._is_sep():
                if not self.has_next() and not self._is_sep(): self._current+=self._text[self._i]
                return self._current
            self._current+=self._c()
            self._nc()


class Command:

    def __init__(self, cmd=None, args=[], cb=Callback(), js=None):
        if not js:
            self.id=str(uuid.uuid4())
            self.cmd=cmd
            self.args=args
        else:
            self.id = js["id"]
            self.cmd = js["cmd"]
            self.args = js["args"]
        self.callback=cb

    def json(self):
        return {
            "id": self.id,
            "cmd": self.cmd,
            "args": self.args
        }

    def response(self, resp):
        self.callback.call((resp,) )

    @staticmethod
    def halt(): return Command("halt")

    @staticmethod
    def reboot(): return Command("reboot")

    @staticmethod
    def print(title, msg): return Command("print", (title, msg))

    @staticmethod
    def from_text(txt):
        l = Lexer(txt)
        cmd = l.next()
        args = []
        while l.next() != None and l.peak() != "":
            args.append(l.peak().rstrip())
        return Command(cmd,args)

    @staticmethod
    def from_js(js):
        return Command(js["cmd"], js["args"])

    def start(self, server):
        x=call(server, self.cmd, self.args)
        if isinstance(x, CommandReturn):
            x.setid(self.id)
        else:
            x=CommandReturn(-1, "")
            x.setid(self.id)
        return x
