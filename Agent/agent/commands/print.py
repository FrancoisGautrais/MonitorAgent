import os
import sys
from inspect import getmembers, isfunction
from agent.commandreturn import CommandReturn
from agent import errors
from utils import execSystem
from conf import Globals
from .utils import start_thread

def _print(shell, title, message):
    os.environ["ZENITY_DATADIR"]=os.path.abspath(Globals.ZENITY + "\\..\\..\\share\\zenity\\")
    if Globals.isWindows():
        wd = os.getcwd()
        os.chdir(os.path.abspath(Globals.ZENITY+"\\..\\.."))
    try:
        execSystem([Globals.ZENITY,  '--error',  '--text='+message,  '--title='+title])
    except FileNotFoundError as err:
        if Globals.isWindows(): os.chdir(wd)
        return CommandReturn(errors.MALFORMED_REQUEST, "Zenity Not found")
    if Globals.isWindows():  os.chdir(wd)


def cmd_print(shell, text):
    title, message = tuple(text)

    start_thread(_print, (shell, title, message))

    return CommandReturn(errors.OK, "")


