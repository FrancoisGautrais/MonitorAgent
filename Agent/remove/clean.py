from gloabls import Globals
from os import walk
import os

_exclude=[line.rstrip('\n') for line in open(Globals.conf('exclude'))]
_include=[line.rstrip('\n') for line in open(Globals.conf('include'))]

print(_include, _exclude)

def comparDir(a, b):
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
                is os.path.
                l.append(os.path.join(x, p))
    return l

def excludeDirs(base, exList):


print(expandDirs(["C:\\Users\\Utilisateur_2\\AppData\\Local\\Programs\\Python\\Python38-32\\Lib\\asyncio"]))