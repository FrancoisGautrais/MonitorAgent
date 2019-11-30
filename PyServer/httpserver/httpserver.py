from .socketwrapper import SocketWrapper, ServerSocket
from .httprequest import HTTPResponse, HTTPRequest, testurl
from threading import Thread

class HttpSocket(SocketWrapper):

    def __init__(self, llsocket, ip=""):
        if isinstance(llsocket, SocketWrapper): llsocket=llsocket._socket
        SocketWrapper.__init__(self, llsocket)
        self.ip=ip

    def _readline(self):
        out=""
        char=self.readc()
        while(char!="\n"):
            out+=char
            char = self.readc()
        return out

    def sendResponse(self, res : HTTPResponse):
        print("res=", res)
        res.addHeader("Content-Length", res.length())
        self.send(res.getbytes())

    def nextrequest(self):
        print("===A===")
        req=self._readHeaders()

        print("===B===")
        if req.method == "GET": return req
        if req.method == "POST": return self._readPostData(req)
        raise Exception("Method '"+req.method+"' non gérée")

    def _readPostData(self, req : HTTPRequest):
        if not req.hasheader("Content-Length"):
            raise Exception("Content-Length field not filled")
        req.data=self.read_str(req.contentLength())
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
            req.headers[key]=val
            line=self._readline()[:-1]
        return req


    @staticmethod
    def fromSocketWrapper(ssocket):
        return HttpSocket(ssocket._socket)

def handlesocket(soc, d=None):
    s=HttpSocket.fromSocketWrapper(soc)
    print(s.nextrequest().__dict__)
    res=HTTPResponse(200, "OK")
    res.setJsonResponse({ "un truc" : [1,2,3]})
    s.sendResponse(res)


class _ThreadWrapper(Thread):

    def __init__(self, fct, obj, data=None):
        Thread.__init__(self)
        self.data=data
        self.obj=obj
        self.fct=fct

    def run(self):
        print("x->", self.obj, self.data)
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
        res=HTTPResponse()
        self.handlerequest(req, res)
        soc.sendResponse(res)
        soc.close()

    def handlerequest(self, req, res):
        pass
