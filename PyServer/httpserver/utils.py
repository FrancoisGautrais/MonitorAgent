
class Callback:

    def __init__(self, fct=None, obj=None, data=None):
        self.fct=fct
        self.obj=obj
        self.data=data


    def call(self, prependParams=(), appendParams=()):
        data=None
        if self.data:
            data=prependParams+(self.data,)+appendParams

        if self.obj:
            if data:
                self.fct(self.obj, *data)
            else:
                x=prependParams+appendParams
                if x:
                    self.fct(self.obj, *x)
                else:
                    self.fct()
        else:
            if data:
                self.fct(*data)
            else:
                x=prependParams+appendParams
                if x:
                    self.fct(*x)
                else:
                    self.fct()