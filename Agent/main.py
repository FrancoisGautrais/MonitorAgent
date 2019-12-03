import requests
from conf import Globals
from remove import clean
import time
from agent.agent import Agent
import sys
import traceback


def doUpdate():
    r=None
    while r==None:
        try:
            r  = requests.post("http://localhost:8080/connect", json=Globals.getAllversionInformation())
            print("A=", r.json())
        except Exception as err:
            r=None
            print("B=", err)
        time.sleep(5)

#doUpdate()

print(Globals.getAllversionInformation())
#client  = Agent()
#client.connect()
"""
while True:
    ret=client.poll()
    client.sendResponse(ret)
"""

for i in range(0,100000):
    r = requests.post("http://localhost:8080/admin/index.html")
    print(r)
    #ret=client.poll()
    #client.sendResponse(ret)


