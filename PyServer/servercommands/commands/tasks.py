from ..commandsloader import CommandReturn
from appserver import AppServer
from appdata import AppData
from command.command import Command
import errors
import time
from ..utils import parse_args

from scheduler import Task



def cmd_sched(server : AppServer, args):
    app = server._clients
    clients = server._clients._clients
    if args[0].lower()=="add":
        tt=time.time()
        arr, args=parse_args(args[1:], {
            "clients": (["-c", "--client"],None),
            "interval": (["-i", "--interval"], -1),
            "start": (["-s", "--start"], time.time()),
            "repeat": (["-r", "--repeat"], -1)
        })
        print("-------->", (time.time()-tt)*1000)
        c=args["clients"]
        if not c:
            c=[]
            for k in clients:
                c.append(k)

        t=Task.interval(c, Command.from_args(arr[0], arr[1:]),
                        float(args["start"]), float(args["interval"]), float(args["repeat"]))
        server._clients.get_scheduler().add_task(t)
    return CommandReturn(0, "")
