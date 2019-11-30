import uuid
import json
from httpserver.utils import Callback

class Command:

    def __init__(self, cmd, args=[], cb=Callback()):
        self.id=uuid.uuid4()
        self.cmd=cmd
        self.args=args
        self.callback=cb

    def json(self):
        return json.dumps({
            "id": self.id,
            "cmd": self.cmd,
            "args": self.args
        })

    def response(self, resp):
        self.callback.call((resp,) )

    @staticmethod
    def halt(): return Command("halt")

    @staticmethod
    def reboot(): return Command("reboot")

    @staticmethod
    def print(title, msg): return Command("print", (title, msg))