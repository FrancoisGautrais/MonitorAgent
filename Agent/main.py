import requests
from conf import Globals
from remove import clean
import time
from agent.agent import Agent
import sys

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
client  = Agent()
client.connect()
time.sleep(1)
client.wait()

"""



client  = Agent()
client.execCommandsFromLine("print a b")
for line in sys.stdin:
    if len(line)>1:
        print(client.execCommandsFromLine(line).out)
"""

