
import sys
sys.path.insert(0, "../Common")
import os
import requests
from conf import Conf
from remove import clean
import time
from agent.agent import Agent
import traceback


def doUpdate():
    r=None
    while r==None:
        try:
            r  = requests.post("http://localhost:8080/connect", json=Conf.getAllversionInformation())
            print("A=", r.json())
        except Exception as err:
            r=None
            print("B=", err)
        time.sleep(5)

#doUpdate()

print(Conf.getAllversionInformation())

ip, port = "", 0
with open("host") as f:
    ip, port=f.read().split("\n")[0].split(":")
    print("her", ip, port)

client  = Agent("http://"+ip+":"+str(port)+"/")

while True:
    os.system("git pull")
    try:
        client.connect()
        while True:
            ret=client.wait()
            client.sendResponse(ret)
    except:
        time.sleep(5)


"""
for i in range(0,100000):
    r = requests.post("http://localhost:8080/admin/index.html")
    print(r)
    #ret=client.poll()
    #client.sendResponse(ret)


"""
