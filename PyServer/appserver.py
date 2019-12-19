import os
import time
from httpserver import socketwrapper
from httpserver.httprequest import HTTPResponse, HTTPRequest
from httpserver.restserver import RESTServer
import errors
import uuid
from appdata import AppData
import json
from command import Command
from client import Client
from httpserver.utils import Callback
from servercommands.commandsloader import CommandReturn
from scheduler import Task, Scheduler
import pystache



def html_template(path, data):
    with open(path) as file:
        return pystache.render(file.read(), data)

ALLOWED=["/admin/login.html", "/admin/css/", "/admin/js/"]

def find_html():
    out=[]
    for k in os.listdir("www/"):
        if k.endswith(".html"):
            out.append("/admin/"+k)
    return out



MOUSTACHES_FILES=find_html()
MOUSTACHE_CLIENT_DATA=["/admin/poste.html"]


class AppServer2(RESTServer):
    def __init__(self, ip="localhost"):
        RESTServer.__init__(self, ip)
        self.static("/admin", "www")

"""
    Gère les connexions réseaux:
        - les clients (agent)
        - Les admnistrateurs (via l'application web) 
"""
class AppServer(RESTServer):

    def __init__(self, ip="localhost"):
        RESTServer.__init__(self, ip)
        self._clients=AppData.load()
        self._connected={}
        self._admins={}

        self._clients.get_scheduler().main_loop_in_thread()

        self.route("POST", "/connect", AppServer.on_connect, self)
        self.route("GET", "/poll", AppServer.on_poll, self)
        self.route("GET", "/wait", AppServer.on_wait, self)
        self.route("PUT", "/file", AppServer.on_put_file, self)
        self.route("GET", "/file/#id", AppServer.on_get_file, self)
        self.route("POST", "/result", AppServer.on_result, self)
        self.route("GET", "/result/#clientid/#cmdid", AppServer.on_get_result, self)
        self.route("GET", "/admin/login", AppServer.admin_on_auth, self)
        self.route("GET", "/admin/disconnect", AppServer.admin_on_disconnect, self)
        self.route("POST", "/admin/command", AppServer.admin_on_command, self)
        self.route("POST", "/admin/command/texte", AppServer.admin_on_command_texte, self)
        self.route("POST", "/admin/server/command", AppServer.admin_on_server_command, self)

        self.route(["GET", "POST"], MOUSTACHES_FILES, AppServer.admin_moustache, self)
        self.static("/admin", "www", authcb=Callback(AppServer.is_authorized, self),
                    needauthcb=Callback(AppServer.need_auth, self))

    """
        Renvoie la liste des clients (si id=None), sinon le client d'id de 'id'
    """
    def clients(self, id=None):
        return self._clients.clients()

    """
        Retire le client id
    """
    def remove_client(self, id):
        for k in self._connected:
            if self._connected[k].id==id:
                del self._connected[id]
                self._clients.remove_client(id)
                return True
        return False

    """
        Vérifie si l'utilisateur a besoin d'une autorisationpour avoir accès a un contenu
    """
    def need_auth(self, req, res):
        for k in ALLOWED:
            if req.path.find(k)>=0: return False
        return True

    """
        Vérifie si un utilisateur est autorisé à a voir accès au contenu
    """
    def is_authorized(self, req, res):
        if not "session-id" in req.cookies:
            res.temporary_redirect("/admin/login.html")
            return False
        id=req.cookies["session-id"]
        if not id in self._admins:
            res.temporary_redirect("/admin/login.html")
            return False
        if time.time()>self._admins[id]:
            res.temporary_redirect("/admin/login.html")
            return False

        return True

    """
        Récupère un client via le header
        S'il n'existe pas, la réponse est préparée et None est renvoyé
        Sinon le client est retourné
    """
    def get_client(self, req : HTTPRequest, res : HTTPResponse):
        if not req.header("x-session-id"):
            res.bad_request(errors.ERROR_HTTP, "Le header 'x-seesion-id' n'est pas transmis", [])
            return None
        id= req.header("x-session-id")
        if not id in self._connected:
            res.unauthorized(errors.BAD_SESSION, "Session invalide", [])
            return None

        return self._connected[id]

    """
        Handler de l'API REST qui permet à l'utilisateur d'avoir un ID de session
    """
    def on_connect(self, req : HTTPRequest, res : HTTPResponse):
        data = req.body_json()
        c=self._clients.connect(data)
        id=str(uuid.uuid4())
        self._connected[id]=c
        c.status=Client.STATUS_CONNECTED
        res.header("x-session-id", id)
        self._clients.save(False)
        c.save()
        res.ok(errors.OK, "OK", None)

    """
        Handler non bloquant de demande de commande
    """
    def on_poll(self, req: HTTPRequest, res: HTTPResponse):
        c=self.get_client(req, res)
        if not c: return
        cmd=c.wait_fo_command(False)
        c.status = Client.STATUS_WAITING
        res.ok(errors.OK, "OK", cmd.json())

    """
        Handler bloquant de demande de commande
    """
    def on_wait(self, req : HTTPRequest, res : HTTPResponse):
        c=self.get_client(req, res)
        if not c: return
        cmd=c.wait_fo_command()
        c.status = Client.STATUS_WAITING
        res.ok(errors.OK, "OK", cmd.json())

    """
        Handler pour gérer les retours des commandes
    """
    def on_result(self, req : HTTPRequest, res : HTTPResponse):
        c=self.get_client(req, res)
        if not c: return

        js=req.body_json()

        ret = c.result(js)
        if ret:
            res.ok(errors.OK, "OK", None)
        else:
            res.not_found(errors.ID_NOT_FOUND, "L'id de la réponse n'existe pas")

    """
        Handler de login de l'administration
    """
    def admin_on_auth(self, req : HTTPRequest, res : HTTPResponse):
        if not req.header("x-user") or not req.header("x-password"):
            return res.bad_request(errors.ERROR_HTTP, "Identifiant non fourni", None)

        if not self._clients.auth(req.header("x-user"),req.header("x-password")):
            return res.unauthorized(errors.ERROR_HTTP, "Mot de passe ou login invalid", None)

        id=str(uuid.uuid4())
        t=100000
        self._admins[id]=time.time()+t
        res.header("Set-Cookie", "session-id="+id+"; Max-Age="+str(t))

    """
        Handler de déconnexion de l'administration
    """
    def admin_on_disconnect(self, req : HTTPRequest, res : HTTPResponse):
        res.header("Set-Cookie", "token = deleted; path = /; expires = Thu, 01 Jan 1970 00: 00:00 GMT")

        if not "session-id" in req.cookies:
            res.temporary_redirect("/admin/login.html")
            return False
        id=req.cookies["session-id"]
        if not id in self._admins:
            res.temporary_redirect("/admin/login.html")
            return False

        del self._admins[id]

    """
        Handler de commande pour le serveur
    """
    def admin_on_server_command(self,req : HTTPRequest, res : HTTPResponse):
        if not self.is_authorized(req, res): return
        data = req.body_json()
        cmd=Command.from_text(data["cmd"])
        out=cmd.start(self).json()
        res.ok(errors.OK, "OK", out)

    """
        Handler de commande pour les clients (en mode texte)
    """
    def admin_on_command_texte(self, req: HTTPRequest, res: HTTPResponse):
        if not self.is_authorized(req, res): return
        data = req.body_json()
        cmd = Command.from_text(data["cmd"])
        self._on_command(cmd, req, res)

    """
        Handler de commande pour les clients (en mode json)
    """
    def admin_on_command(self, req: HTTPRequest, res: HTTPResponse):
        if not self.is_authorized(req, res): return
        data = req.body_json()
        cmd = Command.from_js(data["cmd"])
        self._on_command(cmd, req, res)

    """
        Gère l'envoie des commande aux clients
    """
    def _on_command(self, cmd, req : HTTPRequest, res : HTTPResponse):
        data = req.body_json()
        id = data["target"]
        sync = data["sync"]
        if not id in self._clients._clients:
            return res.not_found(errors.ID_NOT_FOUND, "Id " + id + " not found", None)

        c = self._clients._clients[id]
        c.send(cmd)
        if sync:
            r = c.find_response(cmd.id)
            while not r:
                time.sleep(0.01)
                r = c.find_response(cmd.id)
            res.ok(errors.OK, "OK", r)
        else:
            res.ok(errors.OK, "OK", CommandReturn(errors.OK, "").json())

    """
        Retourne les infos à donner à Moustache (html)
    """
    def get_moustache_data(self):
        out={}
        arr=[]
        for k in self._clients:
            arr.append(self._clients[k].get_moustache_data())
        out["clients"]=arr
        out["clientscount"]=len(out)
        return out

    """
        Handler pour les fichier HTML à générer avec moustache
    """
    def admin_moustache(self,  req : HTTPRequest, res : HTTPResponse):
        needAuth=True
        for k in ALLOWED:
            if req.path.startswith(k):
                needAuth=False
                break
        if needAuth:
            if not self.is_authorized(req, res): return

        path=os.path.abspath("www/"+req.path[7:])
        data=self.get_moustache_data()
        if req.path in MOUSTACHE_CLIENT_DATA:
            post=req.body_json()
            if not "id" in post:
                return res.bad_request(errors.ERROR_HTTP, "Le champs id n'est pas fourni (post)", None)
            if not post["id"] in self._clients._clients:
                return res.bad_request(errors.ID_NOT_FOUND, "L'id "+str(post["id"])+" est incorrecte", None)
            data=self._clients._clients[post["id"]].get_moustache_data()
        res.end(html_template(path, data))

    """
        Handler bloquant de récupération de résultat des commande  
    """
    def on_get_result(self, req : HTTPRequest, res : HTTPResponse):
        if not self.is_authorized(req, res): return
        cid=req.params["clientid"]
        cmdid=req.params["cmdid"]
        if not self._clients.has(cid):
            return res.not_found(errors.ID_NOT_FOUND, "Client not found", None)

        client=self._clients[cid]

        if not client.has_command(cmdid):
            return res.not_found(errors.ID_NOT_FOUND, "Command not found", None)

        r=client.find_response(cmdid)
        while not r:
            time.sleep(0.01)
            client.find_response(cmdid)

        res.ok(errors.OK, "OK", r)

    """
        Handler pour envoyer les fichiers mis à disposition téléchargement
    """
    def on_get_file(self, req : HTTPRequest, res : HTTPResponse):
        id=req.params["id"]
        path="download/"+id
        if not self._clients.has_file(id):
            return res.not_found(errors.FILE_NOT_FOUND, "Not found", None)

        res.header("Content-Disposition", 'attachment; filename="'+self._clients.get_file_info(id)["filename"]+'"')
        res.serve_file(path)
        os.remove(path)
        self._clients.remove_file(id)

    """
        Handler pour récupéerer les fichiers à mettre disponible aux téléchargement
    """
    def on_put_file(self, req : HTTPRequest, res : HTTPResponse):
        c=self.get_client(req, res)
        id=str(uuid.uuid4())
        path = "download/" + id

        with open(path, "wb") as f:
            f.write(req.data)
            self._clients.add_file(id, req.header("x-filename"), c.id)
            return res.ok(errors.OK, "OK", id)
        return res.unauthorized(errors.ERROR_HTTP, "", "Unknown error")