import requests
from conf import Globals
from remove import clean
import time
from agent.agent import Agent
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
time.sleep(5)
client.poll()
print("end")
clean.clean()




