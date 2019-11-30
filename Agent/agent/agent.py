from conf import Globals
import requests
from agent import errors
from .shell import Shell

class Agent:

    def __init__(self, server="http://localhost:8080/"):
        self._baseUrl=server
        self._id=None
        self._shell=Shell(self)

    def connect(self):
        print("Request: ", self._baseUrl+"connect")
        r = requests.post(self._baseUrl+"connect", json=Globals.getAllversionInformation())
        print(r)
        ret = r.json()
        code=ret["code"]
        message=ret["message"]
        self._id=r.headers["x-session-id"]
        print(code, message)
        print(r.json())

    def wait(self): return self._poll("wait")
    def poll(self): return self._poll("poll")

    def _poll(self, url):
        print("Request: ", self._baseUrl+url)
        headers={ "x-session-id" : self._id}
        r = requests.get(self._baseUrl+url, headers=headers)
        ret = r.json()
        code=ret["code"]
        message=ret["message"]
        print(ret)

        if r.status_code==errors.BAD_SESSION or r.status_code==errors.BAD_PARAMETER:
            self.connect()
            return self._poll(url)
        else:
            data=ret["data"]
            if data:
                return self.execCommands(data)
            return None

    def getInfo(self):
        print("Request: ", self._baseUrl + "poll")
        headers = {"x-session-id": self._id}
        r = requests.get(self._baseUrl + "getinfo", headers=headers)
        ret = r.json()
        print(ret)

    def execCommands(self, cmd):
        return self._shell.execCommand(cmd)


    def execCommandsFromLine(self, cmd):
        return self._shell.execCommandFromLine(cmd)
