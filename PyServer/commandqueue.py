import time
import asyncio
class CommandQueue:

    def __init__(self, blocking=True):
        self.queue=[]
        self.cond = asyncio.Condition()

    def enqueue(self, v):
        self.queue.append(v)
        if len(self.queue)==1:
            try:
                self.cond.release()
            except:
                pass
        return v

    def dequeue(self, blocking=True):
        if blocking:
            async with self.cond:
                await self.cond.wait()

            return self.queue.pop(0)

        elif len(self.queue)>0:
            return self.queue.pop(0)
        return None


