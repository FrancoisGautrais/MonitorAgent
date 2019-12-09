from .socketwrapper import SocketWrapper, ServerSocket
from .httprequest import HTTPResponse, HTTPRequest, testurl, HTTP_OK, STR_HTTP_ERROR, HTTP_NOT_FOUND
from threading import Thread

#_val=open("request", "rb").read()

import os



class _ThreadWrapper(Thread):

    def __init__(self, fct, obj, data=None):
        Thread.__init__(self)
        self.data=data
        self.obj=obj
        self.fct=fct

    def run(self):
        self.fct(self.obj, self.data)

def _start_thread(fct, obj, data):
    t=_ThreadWrapper(fct, obj, data)
    t.start()
    #fct(obj, data)

    return t
import time

import socket
class HTTPServer(ServerSocket):

    def __init__(self, ip="localhost"):
        ServerSocket.__init__(self)
        self._ip=ip


    def listen(self, port):
        self._port = port
        self.bind(self._ip, self._port)
        while True:
            x=super().accept()
            req = HTTPRequest(x)
            _start_thread( HTTPServer._handlerequest, self, req)

    def _handlerequest(self, req : HTTPRequest):
        req.parse()
        res=HTTPResponse(200, )
        x=time.time()*1000
        self.handlerequest(req, res)

        res.write(req.get_socket())
        req.get_socket().close()

    def handlerequest(self, req, res):
        pass


    def serve_file(self, req: HTTPRequest, res : HTTPResponse):
        res.serve_file(os.path.join(self.www_dir, req.path[1:]))
