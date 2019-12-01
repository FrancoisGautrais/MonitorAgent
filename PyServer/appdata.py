from client import Client

class AppData:

    def __init__(self):
        self._clients={}
        self._admin={
            "fanch" : {
                "password": "password"
            }
        }

    def connect(self, info):
        if info["uuid"] in self._clients:
            return self._clients[info["uuid"]]

        c=Client(info)
        self._clients[str(c.id)]=c
        return c

    def has(self, id):
        return id in self._clients

    def __iter__(self):
        return self._clients.__iter__()

    def auth(self, login, password):
        return (login in self._admin) and (self._admin[login]["password"]==password)

    def __getitem__(self, id):
        return self._clients[id]

    def findResponse(self, id):
        for c in self._clients:
            x=c.findResponse(id)
            if x: return x
        return None
