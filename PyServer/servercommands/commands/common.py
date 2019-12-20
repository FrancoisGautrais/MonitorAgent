from ..commandsloader import CommandReturn
from appserver import AppServer
from appdata import AppData
import errors

def cmd_print(server : AppServer, args):
    if isinstance(args, str): args=[args]
    print(*args)
    return CommandReturn(0, "")

def cmd_save(server : AppServer, args):
    if not args:
        server.clients().save()
    elif len(args)>0:
        if args[0]=="all":
            server.clients().save()
        elif args[0]=="server":
            server.clients().save(False)
        elif args[0]=="remove":
            AppData.remove_save()
        elif args[0]=="help":
            return CommandReturn(0, "save [server|all|remove]")
    return CommandReturn(0, "")

def _client_info(c):
    out=""
    for k in c.info:
        out+=k+": '"+str(c.info[k])+"'\r\n"
    return out

def cmd_client(self : AppServer, args):

    if len(args)==0:
        out=""
        for i in self.clients():
            c=self.clients(i)
            out+=c.id+" : "+c.info["name"]+"\n"
        return CommandReturn(errors.OK, out)
    if args[0]=="help":
        return CommandReturn(errors.OK, "client ID (info) \nclient help")
    id = args[0]
    if not (id in self.clients()): return CommandReturn(errors.ID_NOT_FOUND, "client '"+id+"' not found")
    c = self.clients(id)
    if len(args)==1: return CommandReturn(errors.OK, _client_info(c))

    if args[1] == "info": return CommandReturn(errors.OK, _client_info(c))
    elif args[1] == "remove":
        self.remove_client(id)
        return CommandReturn(errors.OK, id)

