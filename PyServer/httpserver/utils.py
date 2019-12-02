
import magic
from threading import Lock
_mime_lock=None

if not _mime_lock:
    _mime_lock=Lock()

def mime(path):
    try:
        _mime_lock.acquire()
        x=magic.detect_from_filename(path)
        mi= x.mime_type
        _mime_lock.release()
        return mi
    except:
        return "text/plain"

class Callback:

    def __init__(self, fct=None, obj=None, data=None):
        self.fct=fct
        self.obj=obj
        self.data=data


    def call(self, prependParams=(), appendParams=()):
        data=None
        if not self.fct: return None
        if self.data:
            data=prependParams+(self.data,)+appendParams

        if self.obj:
            if data:
                return self.fct(self.obj, *data)
            else:
                x=prependParams+appendParams
                if x:
                    return self.fct(self.obj, *x)
                else:
                    return self.fct()
        else:
            if data:
                return self.fct(*data)
            else:
                x=prependParams+appendParams
                if x:
                    return self.fct(*x)
                else:
                    return self.fct()