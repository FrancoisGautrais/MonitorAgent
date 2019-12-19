
import uuid

from conf import Conf
if Conf.is_agent():
    from agent.commandsloader import call
    from agent.commandreturn import CommandReturn
else:
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

    def _isSep(self, c=None):
        if c==None:
            c=self._c()
        return c in " \t\r\n"

    def hasNext(self):
        return self._i!=len(self._text)-1 and len(self._text)>0

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
                if not self.hasNext() and not self._isSep(): self._current+=self._text[self._i]
                return self._current
            self._current+=self._c()
            self._nc()

class Command:

    def __init__(self, js):
        if Conf.is_server():
            self.id=js["id"] if ("id" in js) else str(uuid.uuid4())
        else:
            self.id = js["id"]
        self.cmd=js["cmd"]
        self.args=js["args"] if ("args" in js) else []

        #ttd: time to dead : timestamp à laquelle la commande n'est plus valide
        # -1 ou ttd>= time.time()= toujours valide
        # 0 ou ttd<time.time() = commande invalide
        self.ttd=js["ttd"] if ("ttd" in js ) else -1

    """
    def __init__(self, cmd=None, args=[], js=None):
        if not js:
            self.id=str(uuid.uuid4())
            self.cmd=cmd
            self.args=args
            self.ttd=0
        else:
            self.id = js["id"]
            self.cmd = js["cmd"]
            self.args = js["args"]
            self.ttd= js["ttd"] if ("ttd" in js) else 0
    """
    def copy(self):
        return Command(self.json())

    def json(self):
        return {
            "id" : self.id,
            "cmd" : self.cmd,
            "args" : self.args,
            "ttd" : self.ttd
        }

    def start(self, shell):
        x=call(shell, self.cmd, self.args)
        if isinstance(x, CommandReturn):
            x.setid(self.id)
        else:
            x=CommandReturn(-1, "No result")
            x.setid(self.id)
        return x


    @staticmethod
    def from_text(txt):
        l=Lexer(txt)
        cmd=l.next()
        args=[]
        while l.next()!=None and l.peak()!="":
            args.append(l.peak().rstrip())

        return Command.from_js({
            "id": uuid.uuid4(),
            "cmd": cmd,
            "args": args,
            "ttd" :  -1
        })

    @staticmethod
    def halt(): return Command("halt")

    @staticmethod
    def reboot(): return Command("reboot")

    @staticmethod
    def print(title, msg): return Command("print", (title, msg))


    @staticmethod
    def from_js(js):
        return Command(js)

    def from_args(cmd, args):
        return Command.from_js({
            "id": uuid.uuid4(),
            "cmd": cmd,
            "args": args,
            "ttd" :  -1
        })

