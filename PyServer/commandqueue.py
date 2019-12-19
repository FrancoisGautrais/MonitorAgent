import time
import asyncio
from command.command import Command

from threading import Condition, Lock
class CommandQueue:

    def __init__(self, js=None):
        self.queue=[]
        if js:
            queue=js
            for cmd in queue:
                self.queue.append(Command.from_js(cmd))
        self._lock=Lock()

    def json(self):
        out=[]
        for cmd in self.queue:
            out.append(cmd.json())
        return out

    def isempty(self):
        return len(self.queue)==0

    def enqueue(self, v):
        self.queue.append(v)
        if self._lock.locked(): self._lock.release()
        return v

    def dequeue(self, blocking=True):
        if blocking:
            while self.isempty(): self._lock.acquire()
            if self._lock.locked(): self._lock.release()

            return self.queue.pop(0)

        elif len(self.queue) > 0:
            return self.queue.pop(0)
        return None

    def has(self, id):
        for cmd in self.queue:
            if cmd.id==id:
                return True
        return False



