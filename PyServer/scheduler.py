from command.command import Command
import time
import uuid
from threading import Lock
from httpserver.httpserver import start_thread, Callback

class Task:

    def __init__(self, clients, cmd:Command):
        if isinstance(clients, str): clients=[clients]
        self._cmd=cmd
        self._id=str(uuid.uuid4())
        self._clients=clients
        self._start_time=0
        self._interval=0
        self._repeat=0
        self._done=0
        self._task_type=Task.INTERVAL
        self._cmd_ttd=0

    def json(self):
        return {
            "cmd"       : self._cmd.json(),
            "id"        : self._id,
            "clients"   : self._clients,
            "start_time": self._start_time,
            "interval"  : self._interval,
            "repeat"    : self._repeat,
            "done"      : self._done,
            "type"      : self._task_type,
            "cmd_ttd"      : self._cmd_ttd
        }

    @staticmethod
    def from_json(js):
        t=Task(js["clients"], Command.from_js(js["cmd"]))
        t._id=js["id"]
        t._start_time=js["start_time"]
        t._interval=js["interval"]
        t._repeat=js["repeat"]
        t._done=js["done"]
        t._task_type=js["type"]
        t._cmd_ttd=js["cmd_ttd"]
        return t

    def next_deadline(self):
        if self._task_type==Task.INTERVAL:
            if self._repeat>0 or self._repeat<0:
                return self._start_time+(self._done*self._interval)
        return 0

    def done(self):
        self._done+=1
        if self._repeat>0:
            self._repeat-=1
            if self._repeat==0:
                return False
        return True

    def get_new_command(self):
        x=self._cmd.copy()
        if x.ttd>0 and self._cmd_ttd>0:
            x.ttd=time.time()+self._cmd_ttd
        return x

    @staticmethod
    def interval(clientsid, cmd : Command, start=time.time(), interval=-1, repeat=-1):
        t=Task(clientsid, cmd)
        t._start_time=start
        t._interval=interval
        t._repeat=repeat
        return t

Task.INTERVAL="interval"


class Scheduler:

    def __init__(self, app, js=None):
        self._queue=[]
        self._tasks={}

        self._app=app
        self._lock=Lock()
        self._sleep_lock=Lock()
        self._thread=None

        if js:
            self._queue=js["queue"]
            x=js["tasks"]
            for id in x:
                self._tasks[id]=Task.from_json(x[id])

    def json(self):
        out={}
        for id in self._tasks:
            out[id]=self._tasks[id].json()
        return {
            "queue" : self._queue,
            "tasks" : out
        }

    def _insert_in_queue(self, task : Task):
        tasktime=task.next_deadline()
        self._lock.acquire()
        for i in range(len(self._queue)):
            t, n = self._queue[i]
            if tasktime<n:
                self._queue.insert(i, (task._id, tasktime))
                return
        self._queue.append((task._id, tasktime))
        if len(self._queue)==0: self.signal()
        self._lock.release()
        self.signal()

    def _peak(self):
        if len(self._queue):
            id, n = self._queue[0]
            return (self._tasks[id], n)

    def add_task(self, task : Task):
        self._lock.acquire()
        self._tasks[task._id]=task
        self._lock.release()
        self._insert_in_queue(task)

    def signal(self):
        print("signal")
        if self._sleep_lock.locked():
            self._sleep_lock.release()

    def wait_for_signal(self, n=None):
        print("wait", n)
        #self._sleep_lock.acquire()
        if n==None:
            self._sleep_lock.acquire()
        elif n >0:
            self._sleep_lock.acquire(timeout=n)

    def schedule(self):
        task, n = self._peak() if (len(self._queue)>0) else (None,0)
        now=time.time()

        print("Next event ", n, n-now)
        if task:
            if n>now:
                self.wait_for_signal(n-now)
                return

            for cid in task._clients:
                print("Sent to "+cid)
                client=self._app.clients(cid)
                client.send(task.get_new_command())

            self._queue.pop(0)
            if task.done():
                self._insert_in_queue(task)
            else:
                del self._tasks[task._id]
        else:
            self.wait_for_signal()

    def main_loop(self):
        while True:
            self.schedule()

    def main_loop_in_thread(self):
        self._thread=start_thread( Callback(Scheduler.main_loop, self))

