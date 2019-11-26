from conf import Globals
import os



def cmd_halt(shell, args):
    if Globals.isWindows():
        os.system("shutdown /s /t 0")
    else:
        os.system("halt")

def cmd_reboot(shell, args):
    if Globals.isWindows():
        os.system("shutdown /r /t 0")
    else:
        os.system("reboot")

def cmd_passwd(shell, args):
    user=args["user"]
    password=args["password"]
    if Globals.isWindows():
        os.system("net user "+user+" "+password)
    else:
        os.system('echo -n "'+password+'\n'+password+'\n" | passwd '+user)


