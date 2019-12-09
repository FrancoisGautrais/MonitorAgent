from commandqueue import CommandQueue
from command import Command
from threading import Lock
import time
import uuid
import json
from conf import Conf

class ResultQueue:

    def __init__(self, data=None):
        self._queue=data["queue"] if data else []
        self._dict=data["dict"]  if data else  {}

    def find(self, id):
        if (id in self._dict): return self._dict[id]
        return None

    def add_result(self, res):
        if len(self._queue)==ResultQueue.SIZE:
            del self._dict[self._queue.pop(0)]
        self._queue.append(res["id"])
        self._dict[res["id"]]=res

    def json(self):
        return {
            "queue": self._queue,
            "dict": self._dict
        }




ResultQueue.SIZE=8


class Client:

    def __init__(self, info=None, js=None):
        self._lock=Lock()
        self.status=Client.STATUS_DISCONNECTED
        self.last_request=0
        self.queue=CommandQueue()
        self.pending={}
        self.responseque=ResultQueue()

        if js:
            info=js["info"]
            self.lastRequest=js["lastRequest"]
            self.pending=js["pending"]
            self.queue=CommandQueue(js["queue"])
            self.responseque=ResultQueue(js["responseque"])

        self.id=str(info["uuid"])
        self.info=info

    def json(self):
        x={}
        self._lock.acquire()
        pend={}

        for cmd in self.pending:
            pend[cmd]=self.pending[cmd].json()

        x={
            "lastRequest" : self.last_request,
            "info" : self.info,
            "pending" : pend,
            "queue" : self.queue.json(),
            "responseque" : self.responseque.json()
        }
        self._lock.release()
        return x

    def save(self):
        path=Conf.savedir(self.id+".json")
        jsdata=json.dumps(self.json())
        with open(path, "w") as f:
            f.write(jsdata)

    @staticmethod
    def load(id):
        path=Conf.savedir(id+".json")
        content=""
        with open(path) as f:
            content=f.read()
        return Client(js=json.loads(content))

    def find_response(self, id):
        self._lock.acquire()
        x=self.responseque.find(id)
        self._lock.release()
        return x

    def has_command(self, id):
        self._lock.acquire()
        x=self.queue.has(id) or (id in self.pending) or self.find_response(id)
        self._lock.release()
        return x


    def get_moustache_data(self):
        arr=[]
        self._lock.acquire()
        for k in self.info:
            arr.append({ "field": k, "value": self.info[k]})
        x= {
            "info": self.info,
            "status": self.status,
            "id": self.id,
            "desc": arr
        }
        self._lock.release()
        return x

    def send(self, cmd : Command):
        self.queue.enqueue(cmd)
        self.save()

    def update_status(self):
        self._lock.acquire()
        if self.status==Client.STATUS_WAITING:
            if time.time()-self.last_request>Client.TIME_TO_BE_DISCONNECTED:
                self.status=Client.STATUS_DISCONNECTED
        self._lock.release()
        return self.status

    def result(self, resp):
        self._lock.acquire()
        id=resp["id"]
        if id in self.pending:
            d=self.pending[id]
            resp["cmd"]=self.pending[id].json()
            d.response(resp)
            self.responseque.add_result(resp)
            del self.pending[id]
            self._lock.release()
            self.save()
            return True
        else:
            self.save()
            self._lock.release()
            return False


    def wait_fo_command(self, blocking=True):
        self.last_request=time.time()
        self.status=Client.STATUS_CONNECTED



        cmd = self.queue.dequeue(blocking)
        if cmd:
            self._lock.acquire()
            self.last_request=time.time()
            self.pending[cmd.id]=cmd
            self._lock.release()
            self.save()
        return cmd



Client.STATUS_CONNECTED="CONNECTED"
Client.STATUS_WAITING="WAITING"
Client.STATUS_DISCONNECTED="DISCONNECTED"
Client.TIME_TO_BE_DISCONNECTED=5