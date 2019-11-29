import requests
from conf import Globals
from remove import clean
import time
from agent.agent import Agent
from agent.command import Command
import sys
"""
def doUpdate():
    r=None
    while r==None:
        try:
            r  = requests.post("http://192.168.0.17:8080/connect", json=Globals.getAllversionInformation())
            print("A=", r.json())
        except Exception as err:
            r=None
            print("B=", err)
        time.sleep(5)

doUpdate()

"""

client  = Agent()
client.connect()
time.sleep(1)
client.poll()
client.getInfo()
print("end")
clean.clean()




client  = Agent()
x=Command.fromText("print salut 'ok ça va ?' ")
client.execCommands(x)
for line in sys.stdin:
    print("here")
    client.execCommands(Command.fromText(line))
    print("here 2")



