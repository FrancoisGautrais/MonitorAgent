from .socketwrapper import SocketWrapper, ServerSocket
from .httprequest import HTTPResponse, HTTPRequest, testurl, HTTP_OK, STR_HTTP_ERROR, HTTP_NOT_FOUND
from threading import Thread

import os
class HttpSocket(SocketWrapper):

    def __init__(self, llsocket, ip=""):
        if isinstance(llsocket, SocketWrapper): llsocket=llsocket._socket
        SocketWrapper.__init__(self, llsocket)
        self.ip=ip
        self.www_dir=os.path.abspath(".")

    def _readline(self):
        out=""
        char=self.readc()
        while(char!="\n"):
            out+=char
            char = self.readc()
        return out



    def sendResponse(self, res : HTTPResponse):
        total=0

        if res.isStreaming():
            chunk=64*1024
            left=int(res.headers["Content-Length"])
            total+=self.send(res.getheadersbytes())
            while left>0:
                toRead=min(left, chunk)
                readed=self.send(res.data.read(toRead))
                total+=readed
                left-=toRead
        else:
            res.addHeader("Content-Length", res.length())
            d=res.getbodybytes()
            self.send(res.getheadersbytes()+(d if d else bytes()))

            try:
                if d:  self.send(d)
            except Exception as err:
                print(err, self.sent, res.headers["Content-Length"])
                print(str(res.getheadersbytes()))

        return total

    def nextrequest(self):
        req=self._readHeaders()
        if req.method in ["GET"]: return req
        if req.method in ["POST", "PUT"]: return self._readPostData(req)
        raise Exception("Method '"+req.method+"' non gérée")

    def _readPostData(self, req : HTTPRequest):
        if not req.hasheader("Content-Length"):
            raise Exception("Content-Length field not filled")
        req.data=self.read_bin(req.contentLength())
        return req

    def _readHeaders(self):
        req=HTTPRequest()
        head=self._readline().split()
        req.method=head[0]
        req.setUrl(head[1])
        req.version=head[2]

        line=self._readline()[:-1]
        while len(line)>0:
            key=line[:line.find(":")]
            val=line[line.find(":")+1:].lstrip()
            req.setheader(key, val)
            line=self._readline()[:-1]
        return req


    @staticmethod
    def fromSocketWrapper(ssocket):
        return HttpSocket(ssocket._socket)



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

    return t


class HTTPServer(ServerSocket):

    def __init__(self, ip="localhost"):
        ServerSocket.__init__(self)
        self._ip=ip


    def listen(self, port):
        self._port = port
        self.bind(self._ip, self._port)
        while True:
            x=super().accept()
            soc= HttpSocket(x)
            _start_thread( HTTPServer._handlerequest, self, soc)

    def _handlerequest(self, soc : HttpSocket):
        req=soc.nextrequest()
        res=HTTPResponse(200, )
        self.handlerequest(req, res)
        soc.sendResponse(res)
        soc.close()

    def handlerequest(self, req, res):
        pass


    def serveFile(self, req: HTTPRequest, res : HTTPResponse):
        res.serveFile(os.path.join(self.www_dir, req.path[1:]))
