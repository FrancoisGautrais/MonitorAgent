
from .appdata import AppData
from httpserver import socketwrapper
from httpserver.httprequest import HTTPResponse, HTTPRequest
from httpserver.restserver import RESTServer
from .client import Client
import uuid
from .appdata import AppData
import json



class AppServer(RESTServer):

    def __init__(self, ip="localhost"):
        RESTServer.__init__(self, ip)
        self._clients=AppData()
        self._connected={}

    def getClient(self, req):


    def on_connect(self, req : HTTPRequest, res : HTTPResponse):
        data = json.loads(req.data)
        c=self._clients.connect(data)
        id=uuid.uuid4()
        self._connected[id]=c
        res.addHeader("x-session-id", id)
        res.setJsonResponse({
            "code": 0,
            "message": "OK"
        })

    def poll(self):






