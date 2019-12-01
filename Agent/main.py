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
client  = Agent()
client.connect()
while True:
    ret=client.wait()
    client.sendResponse(ret)



"""



client  = Agent()
client.execCommandsFromLine("print a b")
for line in sys.stdin:
    if len(line)>1:
        print(client.execCommandsFromLine(line).out)
"""

