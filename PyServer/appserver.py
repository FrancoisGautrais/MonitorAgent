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

class AppServer(RESTServer):

    def __init__(self, ip="localhost"):
        RESTServer.__init__(self, ip)
        self._clients=AppData()
        self._connected={}
        self.route("POST", "/connect", AppServer.on_connect, self)
        self.route("GET", "/poll", AppServer.on_poll, self)
        self.route("GET", "/wait", AppServer.on_wait, self)
        self.route("POST", "/result", AppServer.on_result, self)
        self.route("GET", "/result/#clientid/#cmdid", AppServer.on_get_result, self)
        self.route("GET", "/admin/login", AppServer.admin_on_auth, self)
        self.route("GET", "/admin/disconnect", AppServer.admin_on_disconnect, self)
        self.route("POST", "/admin/command", AppServer.admin_on_command, self)
        self.route(["GET", "POST"], MOUSTACHES_FILES, AppServer.admin_moustache, self)
        self.static("/admin", "www", authcb=Callback(AppServer.isAuthorized, self),
                    needauthcb=Callback(AppServer.needAuth, self))
        self._admins={}
        self._clients.connect({'os': 'Linux', 'osRelease': '4.14.134-1-MANJARO', 'osVersion': '4.14.134-1-MANJARO', 'pythonVersion': '3.7.3', 'version': (0, 0, 0), 'name': 'Fanch-Fixe', 'uuid': 53447160892554})
        self._clients.connect({'os': 'Windows', 'osRelease': '4.14.134-1-MANJARO', 'osVersion': '4.14.134-1-MANJARO', 'pythonVersion': '3.7.3', 'version': (0, 0, 0), 'name': 'Fanch-Fixe', 'uuid': 53447160892555})
        self._clients.connect({'os': 'Windows', 'osRelease': '4.14.134-1-MANJARO', 'osVersion': '4.14.134-1-MANJARO', 'pythonVersion': '3.7.3', 'version': (0, 0, 0), 'name': 'Fanch-Fixe', 'uuid': 53447160892556})
        self._clients.connect({'os': 'Windows', 'osRelease': '4.14.134-1-MANJARO', 'osVersion': '4.14.134-1-MANJARO', 'pythonVersion': '3.7.3', 'version': (0, 0, 0), 'name': 'Fanch-Fixe', 'uuid': 53447160892557})

    def needAuth(self, req, res):
        for k in ALLOWED:
            if req.path.find(k)>=0: return False
        return True

    def isAuthorized(self, req, res):
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

    def getClient(self, req : HTTPRequest, res : HTTPResponse):
        if not req.hasheader("x-session-id"):
            res.bad_request(errors.ERROR_HTTP, "Le header 'x-seesion-id' n'est pas transmis", [])
            return None
        id= req.headers["x-session-id"]
        if not id in self._connected:
            res.unauthorized(errors.BAD_SESSION, "Session invalide", [])
            return None

        return self._connected[id]

    def on_connect(self, req : HTTPRequest, res : HTTPResponse):
        data = json.loads(req.data)
        c=self._clients.connect(data)
        id=str(uuid.uuid4())
        self._connected[id]=c
        res.addHeader("x-session-id", id)
        res.ok(errors.OK, "OK", None)

    def on_poll(self, req: HTTPRequest, res: HTTPResponse):
        c=self.getClient(req, res)
        if not c: return
        cmd=c.wait_fo_command(False)
        res.ok(errors.OK, "OK", cmd.json())

    def on_wait(self, req : HTTPRequest, res : HTTPResponse):
        c=self.getClient(req, res)
        if not c: return
        cmd=c.wait_fo_command()
        res.ok(errors.OK, "OK", cmd.json())


    def on_result(self, req : HTTPRequest, res : HTTPResponse):
        c=self.getClient(req, res)
        if not c: return

        js=req.json()

        ret = c.result(js)
        if ret:
            res.ok(errors.OK, "OK", None)
        else:
            res.not_found(errors.ID_NOT_FOUND, "L'id de la réponse n'existe pas")

    def admin_on_auth(self, req : HTTPRequest, res : HTTPResponse):
        if not req.hasheader("x-user") or not req.hasheader("x-password"):
            return res.bad_request(errors.ERROR_HTTP, "Identifiant non fourni", None)

        if not self._clients.auth(req.headers["x-user"],req.headers["x-password"]):
            return res.unauthorized(errors.ERROR_HTTP, "Mot de passe ou login invalid", None)

        id=str(uuid.uuid4())
        t=100000
        self._admins[id]=time.time()+t
        res.headers["Set-Cookie"]="session-id="+id+"; Max-Age="+str(t)

    def admin_on_disconnect(self, req : HTTPRequest, res : HTTPResponse):
        res.headers["Set-Cookie"] = "token = deleted; path = /; expires = Thu, 01 Jan 1970 00: 00:00 GMT"

        if not "session-id" in req.cookies:
            res.temporary_redirect("/admin/login.html")
            return False
        id=req.cookies["session-id"]
        if not id in self._admins:
            res.temporary_redirect("/admin/login.html")
            return False

        del self._admins[id]


    def admin_on_command(self,req : HTTPRequest, res : HTTPResponse):
        if not self.isAuthorized(req, res): return
        data = json.loads(req.data)
        cmd=Command.fromText(data["cmd"])
        id=data["target"]
        sync=data["sync"]
        if not id in self._clients._clients:
            return res.not_found(errors.ID_NOT_FOUND, "Id "+id+" not found", None)

        c=self._clients._clients[id]
        c.send(cmd)

        if sync:
            r = c.findResponse(cmd.id)
            while not r:
                time.sleep(0.01)
                r=c.findResponse(cmd.id)
            res.ok(errors.OK, "OK", r)

        print(cmd)



    def getMoustacheData(self):
        out={}
        arr=[]
        for k in self._clients:
            arr.append(self._clients[k].getMoustacheData())
        out["clients"]=arr
        out["clientscount"]=len(out)
        return out


    def admin_moustache(self,  req : HTTPRequest, res : HTTPResponse):
        needAuth=True
        for k in ALLOWED:
            if req.path.startswith(k):
                needAuth=False
                break
        if needAuth:
            if not self.isAuthorized(req, res): return

        path=os.path.abspath("www/"+req.path[7:])
        data=self.getMoustacheData()
        if req.path in MOUSTACHE_CLIENT_DATA:
            post=req.getPostParams()
            if not "id" in post:
                return res.bad_request(errors.ERROR_HTTP, "Le champs id n'est pas fourni (post)", None)
            if not post["id"] in self._clients._clients:
                return res.bad_request(errors.ID_NOT_FOUND, "L'id "+str(post["id"])+" est incorrecte", None)
            data=self._clients._clients[post["id"]].getMoustacheData()
        res.end(html_template(path, data))



    def on_get_result(self, req : HTTPRequest, res : HTTPResponse):
        if not self.isAuthorized(req, res): return
        cid=req.restparams["clientid"]
        cmdid=req.restparams["cmdid"]
        if not self._clients.has(cid):
            return res.not_found(errors.ID_NOT_FOUND, "Client not found", None)

        client=self._clients[cid]

        if not client.hasCommand(cmdid):
            return res.not_found(errors.ID_NOT_FOUND, "Command not found", None)

        r=client.findResponse(cmdid)
        while not r:
            time.sleep(0.01)
            client.findResponse(cmdid)

        res.ok(errors.OK, "OK", r)




