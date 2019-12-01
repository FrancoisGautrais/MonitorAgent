from commandqueue import CommandQueue
from command import Command

import time
import uuid

class ResultQueue:

    def __init__(self):
        self._queue=[]
        self._dict={}

    def find(self, id):
        if (id in self._dict): return self._dict[id]
        return None

    def addResult(self, res):
        if len(self._queue)==ResultQueue.SIZE:
            del self._dict[self._queue.pop(0)]
        self._queue.append(res["id"])
        self._dict[res["id"]]=res

ResultQueue.SIZE=8


class Client:

    def __init__(self, info):
        self.id=info["uuid"]
        self.status=Client.STATUS_DISCONNECTED
        self.lastRequest=0
        self.info=info
        self.queue=CommandQueue()
        self.pending={}
        self.responseque=ResultQueue()

    def findResponse(self, id):
        return self.responseque.find(id)

    def hasCommand(self, id):
        return self.queue.has(id) or (id in self.pending) or self.findResponse(id)


    def getMoustacheData(self):
        arr=[]
        for k in self.info:
            arr.append({ "field": k, "value": self.info[k]})
        return {
            "info": self.info,
            "status": self.status,
            "id": self.id,
            "desc": arr
        }

    def send(self, cmd : Command):
        self.queue.enqueue(cmd)

    def updateStatus(self):
        if self.status==Client.STATUS_WAITING:
            if time.time()-self.lastRequest>Client.TIME_TO_BE_DISCONNECTED:
                self.status=Client.STATUS_DISCONNECTED

        return self.status


    def result(self, resp):
        id=resp["id"]
        if id in self.pending:
            d=self.pending[id]
            d.response(resp)
            self.responseque.addResult(resp)
            del self.pending[id]
            return True
        else:
            return False


    def wait_fo_command(self, blocking=True):
        self.lastRequest=time.time()
        self.status=Client.STATUS_CONNECTED



        cmd = self.queue.dequeue(blocking)
        if cmd:
            self.lastRequest=time.time()
            self.status=Client.STATUS_WAITING
            self.pending[cmd.id]=cmd
        return cmd



Client.STATUS_CONNECTED="CONNECTED"
Client.STATUS_WAITING="WAITING"
Client.STATUS_DISCONNECTED="DISCONNECTED"
Client.TIME_TO_BE_DISCONNECTED=5