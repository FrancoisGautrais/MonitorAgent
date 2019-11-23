from conf import Globals
from os import walk
import os


def readFilexClude(path, base=[]):
    current=base.copy()
    for line in open(path):
        line=line.rstrip("\n")
        if os.path.isdir(line) and ((line[-1]!="\\") if Globals.isWindows() else (line[-1]!="/")):
            line+="\\" if Globals.isWindows() else "/"
        current.append(line)
    return current


def comparDir(_a, _b):
    a=""
    b=""
    if len(_a) < len(_b):
        a=_a+""
        b=_b[:len(a)]
    else:
        a=_a[:len(b)]
        b=_b+""

    if Globals.isWindows():
        return a.replace("/","\\").lower()==b.replace("/","\\").lower()
    return a.replace("/","\\")==b.replace("/","\\")

def beginWith(file, base):
    if len(file)>len(base):
        return comparDir(file[:len(base)], base)
    return comparDir(file, base[:len(file)])

def expandDirs(dirs):
    l=dirs
    i=0
    while i<len(l):
        x=l[i]
        i=i+1
        if os.path.isdir(x):
            for p in os.listdir(x):
                p=os.path.join(x,p)
                if os.path.isdir(p):
                    if Globals.isWindows(): p+="\\"
                    else: p+="/"
                l.append(p)
    return l

def excludeDirs(base, exList):
    out=[]
    for file in base:
        for test in exList:
            add=True
            if comparDir(test, file):
                add=False
        if add:
            out.append(file)


    return out



exclude=readFilexClude(Globals.conf("exclude"))
include=expandDirs(readFilexClude(Globals.conf("include")))
fileToDelete=excludeDirs(include, exclude)


def clean():
    print(include)
    print(fileToDelete)
    for i in range(len(fileToDelete)-1, -1, -1):
        file=fileToDelete[i]
        if os.path.isdir(file):
            try:
                os.rmdir(file)
            except: pass
        else:
            os.remove(file)