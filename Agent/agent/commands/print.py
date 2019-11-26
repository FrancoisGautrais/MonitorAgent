import os

def cmd_exec(text):
    title, message = tuple(text)
    os.system('zenity --error --text="'+message+'" --title="'+title+'"')




def load_commands():
    return [("print", cmd_exec)]
