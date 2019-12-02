from client import Client
from conf import  Conf
import json
import os

class AppData:

    def __init__(self, js=None):
        self._clients=js["clients"] if js else {}
        self._files=js["files"] if js else {}
        self._admin=js["admin"] if js else {
            "fanch" : {
                "password": "password"
            }
        }

    def connect(self, info):
        if info["uuid"] in self._clients:
            return self._clients[info["uuid"]]

        c=Client(info)
        self._clients[str(c.id)]=c
        c.save()
        self.save(False)
        return c

    def addFile(self, id, name, client):
        self._files[id]={"filename" : name, "client" : client}
        self.save(False)

    def hasFile(self, id):
        return id in self._files

    def getFileInfo(self, id):
        return self._files[id]

    def removeFile(self, id):
        del self._files[id]
        self.save(False)

    def has(self, id):
        return id in self._clients

    def __iter__(self):
        return self._clients.__iter__()

    def __getitem__(self, id):
        return self._clients[id]

    def auth(self, login, password):
        return (login in self._admin) and (self._admin[login]["password"]==password)

    def removeClient(self, id):
        path=Conf.savedir(id)
        if os.path.isfile(path): os.remove(path)
        del self._clients[id]


    def findResponse(self, id):
        for c in self._clients:
            x=c.findResponse(id)
            if x: return x
        return None

    @staticmethod
    def removeSave():
        path=Conf.savedir("")
        for p in os.listdir(path):

            os.remove(Conf.savedir(p))




    @staticmethod
    def load():
        path=Conf.savedir("server.js")
        if os.path.isfile(path):
            content=""
            with open(path) as f:
                content=f.read()
            cl={}
            content=json.loads(content)
            for c in content["clients"]:
                cl[c]=Client.load(c)
            content["clients"]=cl
            return AppData(js=content)
        return AppData()


    def save(self, all=True):
        out={}
        arr=[]
        tmp={}

        for c in self._clients:
            c=self._clients[c]
            if all: c.save()
            arr.append(c.id)

        for f in self._files:
            o=self._files[f]
            tmp[f]=o

        out["clients"] = arr
        out["files"] = tmp
        out["admin"] = self._admin

        path=Conf.savedir("server.js")
        with open(path, "w") as f:
            f.write(json.dumps(out))




