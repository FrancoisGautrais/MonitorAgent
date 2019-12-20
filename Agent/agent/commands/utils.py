from threading import Thread

class _ThreadWrapper(Thread):

    def __init__(self, fct, data=None):
        Thread.__init__(self)
        self.data=data
        self.fct=fct

    def run(self):
        self.fct(*self.data)

def start_thread(fct, data):
    t=_ThreadWrapper(fct, data)
    t.start()

    return t