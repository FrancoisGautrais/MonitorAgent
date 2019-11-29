import socket
import socketwrapper
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

server=socketwrapper.HTTPServer("127.0.0.1", 8080)
server.route("GET", "/create", socketwrapper.HTTPServer.create,server )
server.route("GET", "/delete", socketwrapper.HTTPServer.delete,server )
server.route("GET", "/update", socketwrapper.HTTPServer.update,server )
server.accept()
