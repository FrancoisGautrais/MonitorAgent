from .commandqueue import CommandQueue
from .command import Command

import time
import uuid

class Client:

    def __init__(self, info):
        self.id=info["uuid"]
        self.status=Client.STATUS_DISCONNECTED
        self.lastRequest=0
        self.info=info
        self.queue=CommandQueue()
        self.pending={}

    def send(self, cmd : Command):
        self.queue.enqueue(cmd)

    def updateStatus(self):
        if self.status==Client.STATUS_WAITING:
            if time.time()-self.lastRequest>Client.TIME_TO_BE_DISCONNECTED:
                self.status=Client.STATUS_DISCONNECTED

        return self.status


    def _on_response(self, resp):
        if resp.id in self.pending:
            d=self.pending[resp.id]
            d.response(resp)
            del self.pending[resp.id]

    def wait_fo_command(self, req, blocking=True):
        self.lastRequest=time.time()
        self.status=Client.STATUS_CONNECTED

        if ("response" in req):
            data=req["response"]
            self._on_response(data)

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