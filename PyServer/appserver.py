import time
from httpserver import socketwrapper
from httpserver.httprequest import HTTPResponse, HTTPRequest
from httpserver.restserver import RESTServer
import errors
import uuid
from appdata import AppData
import json
from client import Client
from httpserver.utils import Callback


class AppServer(RESTServer):

    def __init__(self, ip="localhost"):
        RESTServer.__init__(self, ip)
        self._clients=AppData()
        self._connected={}
        self.route("POST", "/connect", AppServer.on_connect, self)
        self.route("GET", "/poll", AppServer.on_poll, self)
        self.route("GET", "/wait", AppServer.on_wait, self)
        self.route("POST", "/result/#id", AppServer.on_result, self)
        self.route("GET", "/admin/login", AppServer.admin_on_auth, self)
        self.static("/admin", "www", authcb=Callback(AppServer.isAuthorized, self),
                    needauthcb=Callback(AppServer.needAuth, self))
        self._admins={}

    def needAuth(self, req, res):
        return (not req.path.endswith("/admin/login.html")) and req.path.find("/admin/js/")==-1 and req.path.find("/admin/css/")==-1

    def isAuthorized(self, req, res):
        if not "session-id" in req.cookies:
            res.temporary_redirect("login.html")
            return False
        id=req.cookies["session-id"]
        if not id in self._admins:
            res.temporary_redirect("login.html")
            return False
        if time.time()<self._admins[id]:
            res.temporary_redirect("login.html")
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
        res.ok(errors.OK, "OK", cmd)

    def on_wait(self, req : HTTPRequest, res : HTTPResponse):
        c=self.getClient(req, res)
        if not c: return
        cmd=c.wait_fo_command()
        res.ok(errors.OK, "OK", cmd)

    def on_result(self, req : HTTPRequest, res : HTTPResponse):
        c=self.getClient(req, res)
        if not c: return

        js=req.json()
        if not "result" in js:
            return res.bad_request(errors.MALFORMED_REQUEST, "Le résultat n'est pas dans la requete", None)

        ret = c.result(js["result"])
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




