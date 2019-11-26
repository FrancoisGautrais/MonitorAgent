from conf import Globals
import os



def cmd_exec_halt(args):
    if Globals.isWindows():
        os.system("shutdown /s /t 0")
    else:
        os.system("halt")
    print("Commande halt executée")

def cmd_exec_reboot(args):
    if Globals.isWindows():
        os.system("shutdown /r /t 0")
    else:
        os.system("reboot")
    print("Commande reboot executée")


def load_commands():
    return [("halt", cmd_exec_halt), ("reboot", cmd_exec_reboot)]
