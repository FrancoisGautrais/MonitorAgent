import os
import sys
from inspect import getmembers, isfunction

def cmd_print(shell, text):
    title, message = tuple(text)
    os.system('zenity --error --text="'+message+'" --title="'+title+'"')


