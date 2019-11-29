import os
import sys
from inspect import getmembers, isfunction
from agent.commandreturn import CommandReturn
from agent import errors
from utils import execSystem
from conf import Globals

def cmd_print(shell, text):
    title, message = tuple(text)
    wd = os.getcwd()
    os.environ["ZENITY_DATADIR"]=os.path.abspath(Globals.ZENITY + "\\..\\..\\share\\zenity\\")
    print(os.path.abspath(Globals.ZENITY + "\\..\\.."), )
    os.chdir(os.path.abspath(Globals.ZENITY+"\\..\\.."))
    try:
        execSystem([Globals.ZENITY,  '--error',  '--text='+message,  '--title='+title])
    except FileNotFoundError as err:
        os.chdir(wd)
        return CommandReturn(errors.BAD_PARAMETER, "Not found", "Commande 'zenity introuvable")

    os.chdir(wd)
    return CommandReturn(errors.OK, "OK")


