from conf import Globals
import requests
from .command import Command

class Agent:

    def __init__(self, server="http://192.168.0.17:8080/"):
        self._baseUrl=server

    def connect(self):
        print("Here: ", self._baseUrl+"connect")
        r = requests.post(self._baseUrl+"connect", json=Globals.getAllversionInformation())
        ret = r.json()
        code=ret["code"]
        message=ret["message"]
        print(code, message)
        print(r.json())

    def poll(self):
        print("Here: ", self._baseUrl+"poll")
        r = requests.get(self._baseUrl+"poll")
        ret = r.json()
        code=ret["code"]
        message=ret["message"]

        if code==100:
            self.connect()
            return self.poll()
        else:
            data=ret["data"]
            print("data=", data)
            return self.execCommands(data)


    def execCommands(self, cmd):
        out={}
        for c in cmd:
            x=Command(c).start()
            for k in x:
                out[k]=x
        return out
