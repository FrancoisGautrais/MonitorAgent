from client import Client

class AppData():

    def __init__(self):
        self._clients={}

    def connect(self, info):
        if info["uuid"] in self._clients:
            return self._clients[info["uuid"]]

        c=Client(info)
        self._clients[c.id]=c
        return c

    def auth(self, login, password):
        return True

    def __getitem__(self, id):
        return self._clients[id]
