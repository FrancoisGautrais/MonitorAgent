import time
import asyncio
class CommandQueue:

    def __init__(self, blocking=True):
        self.queue=[]
        #self.cond = asyncio.Condition()

    def isempty(self):
        return len(self.queue)==0

    def enqueue(self, v):
        self.queue.append(v)
        return v

    def dequeue(self, blocking=True):
        if blocking:
            while self.isempty(): time.sleep(0.01)

            return self.queue.pop(0)

        elif len(self.queue) > 0:
            return self.queue.pop(0)
        return None

    def has(self, id):
        for cmd in self.queue:
            if cmd.id==id:
                return True
        return False
    """
    async def enqueue(self, v):
        self.queue.append(v)
        if len(self.queue)==1:
            try:
                self.cond.release()
            except:
                pass
        return v
    
    async def dequeue(self, blocking=True):
        if blocking:
            async with self.cond:
                await self.cond.wait()

            return self.queue.pop(0)

        elif len(self.queue)>0:
            return self.queue.pop(0)
        return None
        
    """


