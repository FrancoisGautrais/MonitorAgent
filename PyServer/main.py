from httpserver import socketwrapper
from httpserver.httprequest import HTTPResponse
from httpserver.restserver import RESTServer
from appserver import AppServer
"""
from clientthread import ClientThread

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to a public host, and a well-known port
#serversocket.bind((socket.gethostname(), 8080))
serversocket.bind(("127.0.0.1", 8080))

# become a server socket
serversocket.listen(5)
while True:
    # accept connections from outside
    (clientsocket, address) = serversocket.accept()
    print(clientsocket)
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    ct = ClientThread(clientsocket)
    ct.run()
"""

def test(req, res : HTTPResponse):
    res.end("Default")


server= AppServer()

#server.route("GET", "/create/#x/#y/z", RESTServer.create, server)
#server.route("GET", "/delete", socketwrapper.HTTPServer.delete,server )
#server.route("GET", "/update", socketwrapper.HTTPServer.update,server )
server.listen(8080)
