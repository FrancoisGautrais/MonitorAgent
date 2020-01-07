from conf import Conf
import os
from ..shell import Shell
from utils import execSystem
from ..commandreturn import CommandReturn
from .. import errors
import psutil


def cmd_halt(shell, args):
    if Conf.isWindows():
        os.system("shutdown /s /t 0")
    else:
        os.system("halt")

def cmd_reboot(shell, args):
    if Conf.isWindows():
        os.system("shutdown /r /t 0")
    else:
        os.system("reboot")

def cmd_passwd(shell, args):
    user=args["user"]
    password=args["password"]
    if Conf.isWindows():
        os.system("net user "+user+" "+password)
    else:
        os.system('echo -n "'+password+'\n'+password+'\n" | passwd '+user)


def cmd_killall(self : Shell, args):
    if Conf.isWindows():
        return execSystem(["taskkill", "/F", "/IM", args[0], "/T"])
    else:
        return execSystem(["killall ", args[0]])


def cmd_monitor(self : Shell, args):
    m=psutil.virtual_memory()
    s=psutil.cpu_stats()
    percents=psutil.cpu_percent(0.1, True)
    percent=psutil.cpu_percent()
    freqs=psutil.cpu_freq(True)
    freq=psutil.cpu_freq()
    cpus={
        "count" : len(freqs),
        "global" : {
            "percent": percent,
            "max" : freq.max,
            "min" : freq.min,
            "current" : freq.current

        }
    }
    for i in range(0, len(freqs)):
        cpus[i]={
            "percent": percents[i],
            "max" : freqs[i].max,
            "min" : freqs[i].min,
            "current" : freqs[i].current
        }

    return CommandReturn(errors.OK, {
        "memory": {
            "total": m.total,
            "free": m.free,
            "active": m.active,
            "inactive": 0 if Conf.isWindows() else m.inactive,
            "buffers":  0 if Conf.isWindows() else m.inactive,
            "cached":  0 if Conf.isWindows() else m.inactive
        },
        "cpus" : cpus
    })


def cmd_ps(self: Shell, args):

    all=['status', 'cpu_num', 'num_ctx_switches', 'pid', 'memory_full_info', 'connections', 'cmdline', 'create_time',
         'ionice', 'num_fds', 'memory_maps', 'cpu_percent', 'terminal', 'ppid', 'cwd', 'nice', 'username', 'cpu_times',
         'io_counters', 'memory_info', 'threads', 'open_files', 'name', 'num_threads', 'exe', 'uids', 'gids',
         'cpu_affinity', 'memory_percent', 'environ']
    medium=["cwd", "name", "nice", "status", "pid", "num_fds", "memory_full_info", "exe", "create_time", "num_threads",
     "username", "memory_percent", "cpu_percent", "cmdline", "cpu_times"]
    small = ["name", "nice", "status", "pid", "create_time", "username", "memory_percent", "cpu_percent", "cmdline",
              "cpu_times"]
    tiny = ["name",  "pid", "username", ]


    if len(args)==0:
        args=medium
    elif len(args)==1:
        if args[0]=="medium": args=medium
        if args[0]=="all": args=all
        if args[0]=="small": args=small
        if args[0]=="tiny": args=tiny

    listOfProcessNames = list()
    #['status', 'cpu_num', 'num_ctx_switches', 'pid', 'memory_full_info', 'connections', 'cmdline', 'create_time', 'ionice', 'num_fds', 'memory_maps', 'cpu_percent', 'terminal', 'ppid', 'cwd', 'nice', 'username', 'cpu_times', 'io_counters', 'memory_info', 'threads', 'open_files', 'name', 'num_threads', 'exe', 'uids', 'gids', 'cpu_affinity', 'memory_percent', 'environ']
    for proc in psutil.process_iter():
        pInfoDict = proc.as_dict(attrs=args)
        listOfProcessNames.append(pInfoDict)

    return CommandReturn(errors.OK, listOfProcessNames)