from agent.command import Command
import time



class Task:
    def __init__(self, d):
        self.type=d["type"]
        self.name=d["name"]
        self.id=d["id"]
        self.cmd=Command(d["cmd"]) if isinstance(d["cmd"], dict) else d["cmd"]

    def next_deadline(self):
        raise Exception("Must be overrided")

    def get_next_command(self):
        return self.cmd.copy()
    """
        Retourne Vrai s'il reste une commande à executer
    """
    def done(self):
        raise Exception("Must be overrided")

    def json(self):
        return {
            "name" : self.name,
            "type" : self.type,
            "id" : self.id,
            "cmd" : self.cmd.json()
        }


class OneShotTask(Task):
    TYPE="ONE_SHOT_TASK"
    def __init__(self, d):
        Task.__init__(self, d)
        self.start_time=d["start_time"]

    def next_deadline(self):
        return self.start_time

    def done(self):
        return False

    def json(self):
        up=Task.json(self)
        up.update({"start_time" : self.start_time})
        return up

    def from_timestamp(self):

import datetime

def dict_to_timedelta(d):
    d={ "d" : 0, "h":0, "m":0, "s":0, "ms":0 }.update(d)
    return datetime.timedelta(days=d["d"], hours=d["h"], minutes=d["m"],
                           seconds=d["s"], microseconds=d["ms"])

def dict_to_time(d):
    d={  "h":0, "m":0, "s":0, "ms":0 }.update(d)
    return datetime.time( hour=d["h"], minute=d["m"],
                           second=d["s"], microsecond=d["ms"])

class IntervalTask(Task):
    def __init__(self, name, cmd: Command, interval):


class DailyTask(Task):
    def __init__(self, d):
        Task.__init__(self, d)
        h=hourofday
        self.time=datetime.datetime.today().replace(hour=0, minute=0,
                                                    second=0, microsecond=0)+\
                    datetime.timedelta(hours=h.hour, minutes=h.minute,
                                       seconds=h.second, microseconds=h.microsecond)

    def next_deadline(self):
        return self.time

    def done(self):
        self.time+=datetime.timedelta(days=1)
        return True


    def json(self):
        up=Task.json(self)
        up.update({"start_time" : self.start_time})
        return up

    def from_hour(self, cmd, hour):

class WeeklyTask(Task):
    #sched = [LUNDI, MARDI, MERCREDI...]
    def __init__(self, name, cmd : Command, sched):
        Task.__init__(self, name, cmd)
        now=datetime.datetime.today()
        tnow=now.timestamp()
        self.week_start=now.replace(day=now.day, hour=now.hour, minute=now.minute,
                                    second=now.second, microsecond=now.microsecond)
        self.index=0
        self.times=[]
        for i in range(len(sched)):
            x=sched[i]
            if x:
                x=x if isinstance(x, (list,tuple)) else [x]
                for date in x:
                    self.times.append(
                        self.week_start+datetime.timedelta(days=i, hours=date.hour, minutes=date.minute,
                                                           seconds=date.second, microseconds=date.microsecond)
                    )

        for i in range(len(self.times)):
            if now>(self.week_start+self.times[i]):
                self.index=i+1
        if i==len(self.times):
            self._next_week()

    def _next_week(self):
        self.index=0
        td=datetime.timedelta(days=7)
        for i in range(len(self.times)):
            self.times[i]+=td

    def next_deadline(self):
        return self.times[self.index]

    def done(self):
        self.index+=1
        if self.index>=len(self.times):
            self._next_week()
        return True
