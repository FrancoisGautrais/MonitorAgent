from client import Client
from conf import  Conf
import json
import os


"""
    Gère les données des clients (agent) et authorisation des admins
"""
class AppData:

    def __init__(self, js=None):
        self._clients=js["clients"] if js else {}
        self._files=js["files"] if js else {}
        self._admin=js["admin"] if js else {
            "fanch" : {
                "password": "password"
            }
        }

    """
        Connexion d'un client (agent) 
    """
    def connect(self, info):
        if info["uuid"] in self._clients:
            return self._clients[info["uuid"]]

        c=Client(info)
        self._clients[str(c.id)]=c
        c.save()
        self.save(False)
        return c

    """
        Ajout d'un fichier (afin de le mettre au téléchargement)
    """
    def add_file(self, id, name, client):
        self._files[id]={"filename" : name, "client" : client}
        self.save(False)

    """
        Vérifie si un fichier est disponible
    """
    def has_file(self, id):
        return id in self._files

    """
        Récupère les méta information d'un fichier  mis à disposition au téléchargement
    """
    def get_file_info(self, id):
        return self._files[id]

    """
        Supprime un fichier disponible au téléchargement
    """
    def remove_file(self, id):
        del self._files[id]
        self.save(False)

    """
        Vérifie si un client est enregistré
    """
    def has(self, id):
        return id in self._clients

    def __iter__(self):
        return self._clients.__iter__()

    def __getitem__(self, id):
        return self._clients[id]

    """
        Vérifie l'authentification d'un admin
    """
    def auth(self, login, password):
        return (login in self._admin) and (self._admin[login]["password"]==password)

    """
        Supprime un client (agent)
    """
    def remove_client(self, id):
        path=Conf.savedir(id)
        if os.path.isfile(path): os.remove(path)
        del self._clients[id]

    """
        Recherche une réponse à une commande
    """
    def find_response(self, id):
        for c in self._clients:
            x=c.find_response(id)
            if x: return x
        return None


    """
        Supprime la sauvegarde
    """
    @staticmethod
    def remove_save():
        path=Conf.savedir("")
        for p in os.listdir(path):

            os.remove(Conf.savedir(p))



    """
        Charge les données en revoie un objet initialisé
    """
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

    """
        Sauvegarde les données
    """
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
        jsdata=json.dumps(out)
        with open(path, "w") as f:
            f.write(jsdata)




