def cmd_exec(args):
    print("Commande halt executée")


def load_commands():
    return [("halt", cmd_exec)]
