

class Stack:

    def __init__(self):
        self._data=[]

    def push(self, val):
        self._data.append(val)
        return val

    def pop(self):
        if self.isEmpty(): return None
        return self._data.pop()

    def peak(self):
        if self.isEmpty(): return None
        return self._data[-1]

    def isEmpty(self):
        return len(self._data)==0