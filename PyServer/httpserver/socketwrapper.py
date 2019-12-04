import socket
from threading import Thread
#content=open("request", "rb").read()


import time
class SocketWrapper:
    def __init__(self, llsocket):
        self._socket=llsocket
        self.sent=0


    def send(self, s):
        if isinstance(s, str): s = bytes(s, "utf8")
        return self._socket.sendall(s)

    def read(self, l=1):
        if len==1: return self._socket.recv(1)
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
        return str(self.read(len), encoding="utf8")

    def readline(self):
        out=""
        x=self._socket.recv(1)
        while x[0]!=10:
            out+=x.decode("utf8")
            x = self._socket.recv(1)
        return out

    def readc(self):
        return self.read_str()

    def close(self):
        try:
            self._socket.shutdown(socket.SHUT_WR)
            return self._socket.close()
        except:
            return None





class ServerSocket(SocketWrapper):

    def __init__(self):
        SocketWrapper.__init__(self, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._ip=""
        self._port=-1

    def bind(self, ip, port):
        self._ip=ip
        self._port=port
        print("Listening on", ip, "at port", port,"...")
        self._socket.bind((ip, port))
        self._socket.listen(50)

    def accept(self, cb=None, args=[]):
        (clientsocket, address) = self._socket.accept()
        client = SocketWrapper(clientsocket)
        if cb: cb(client, args)
        return client



