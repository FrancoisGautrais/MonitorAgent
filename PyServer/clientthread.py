import random
import sys
from threading import Thread
import time
import socket
from socketwrapper import

class ClientThread(Thread):

    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, data : socket):
        Thread.__init__(self)
        self._socket = AppSocket(data)


    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        print("Open")
        self._socket.send("Salut")
        print("Open")




