import os
import sys
from inspect import getmembers, isfunction
from agent.commandreturn import CommandReturn
from agent import errors
from utils import execSystem
from conf import Conf
from .utils import start_thread

def _print(shell, title, message):
    os.environ["ZENITY_DATADIR"]=os.path.abspath(Conf.ZENITY + "\\..\\..\\share\\zenity\\")
    if Conf.isWindows():
        wd = os.getcwd()
        os.chdir(os.path.abspath(Conf.ZENITY+"\\..\\.."))
    try:
        execSystem([Conf.ZENITY,  '--error',  '--text='+message,  '--title='+title])
    except FileNotFoundError as err:
        if Conf.isWindows(): os.chdir(wd)
        return CommandReturn(errors.MALFORMED_REQUEST, "Zenity Not found")
    if Conf.isWindows():  os.chdir(wd)


def cmd_print(shell, text):
    title, message = tuple(text)

    start_thread(_print, (shell, title, message))

    return CommandReturn(errors.OK, "")


