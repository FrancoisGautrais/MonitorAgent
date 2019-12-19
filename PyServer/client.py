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

"""
    Représente un Client (agent)
"""
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
            self.queue=CommandQueue(js["queue"])
            """
            self.pending=js["pending"]
            pend=js["pending"]
            for id in pend:
                cmd=pend[id]
                self.pending[id]=Command(js=cmd)
            self.pending={}
            self.responseque=ResultQueue(js["responseque"])
            """

        self.id=str(info["uuid"])
        self.info=info

    """
        Renvoie les données en format JSON
    """
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

    """
        Sauvegarde les données
    """
    def save(self):
        path=Conf.savedir(self.id+".json")
        jsdata=json.dumps(self.json())
        with open(path, "w") as f:
            f.write(jsdata)

    """
        Charge un client depuis son id
    """
    @staticmethod
    def load(id):
        path=Conf.savedir(id+".json")
        content=""
        with open(path) as f:
            content=f.read()

        #try:
        data=json.loads(content)
        return Client(js=data)
        #except Exception as err:
        #    print("Erreur: Impossible de charger le client '"+str(id)+"' : "+str(err))
        #    return None

    """
        Cherche une réponse depuis un id
    """
    def find_response(self, id):
        self._lock.acquire()
        x=self.responseque.find(id)
        self._lock.release()
        return x

    """
        Vérifie si une commande est présente (depuis son id)
    """
    def has_command(self, id):
        self._lock.acquire()
        x=self.queue.has(id) or (id in self.pending) or self.find_response(id)
        self._lock.release()
        return x

    """
        Retourne les données à insérer dans les pages html
    """
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

    """
        Envoie (ajoute à la file d'attente) une commande
    """
    def send(self, cmd : Command):
        self.queue.enqueue(cmd)
        self.save()

    """
        Met à jour le status (de connexion) du client
    """
    def update_status(self):
        self._lock.acquire()
        if self.status==Client.STATUS_WAITING:
            if time.time()-self.last_request>Client.TIME_TO_BE_DISCONNECTED:
                self.status=Client.STATUS_DISCONNECTED
        self._lock.release()
        return self.status

    """
        Réponse à une commande
    """
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

    """
        Fonction qui permet d'attendre (blocking=true) la prochaine commande
    """
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