import socket
from httprequest import HTTPRequest, HTTPResponse
from threading import Thread

class SocketWrapper:

    def __init__(self, llsocket):
        self._socket=llsocket

    def send(self, s):
        if isinstance(s, str): s = bytes(s, "utf8")
        self._socket.send(s)

    def read_bin(self, l=1):
        chunks = []
        bytes_recd = 0
        while bytes_recd < l:
            chunk = self._socket.recv(min(l - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    def read_str(self, len=1):
        return str(self.read_bin(len), encoding="utf8")

    def readc(self):
        return self.read_str()

    def close(self):
        return self._socket.close()


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
        res.addHeader("Content-Length", len(res.data))
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


class ServerSocket(SocketWrapper):

    def __init__(self):
        SocketWrapper.__init__(self, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._ip=""
        self._port=-1

    def bind(self, ip, port):
        self._ip=ip
        self._port=port
        self._socket.bind((ip, port))
        self._socket.listen(5)

    def accept(self, cb=None, args=[]):
        (clientsocket, address) = self._socket.accept()
        client = SocketWrapper(clientsocket)
        if cb: cb(client, args)
        return client

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

    def __init__(self, ip, port):
        ServerSocket.__init__(self)
        self.bind(ip, port)
        self._handlers={}

    def route(self, method, url, fct, obj=None, data=None):
        if not (method in self._handlers):
            self._handlers[method.upper()]={}
        self._handlers[method.upper()][url]=(fct, obj, data)



    def accept(self):
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


    def create(self, req : HTTPRequest, res : HTTPResponse):
        res.end("Create")

    def delete(self, req : HTTPRequest, res : HTTPResponse):
        res.end("update")

    def update(self, req : HTTPRequest, res : HTTPResponse):
        res.end("update")

    def handlerequest(self, req, res):
        m=req.method
        u=req.path
        d=self._handlers[m]
        for url in d:
            if url==u or u+"/"==url or u==url+"/":
                fct, obj, data = d[url]
                if obj:
                    if data:
                        fct(obj, req, res, data)
                    else:
                        fct(obj, req, res)
                else:
                    fct(req, res, data)





