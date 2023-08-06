# This file is in the Public Domain.

def cmd(event):
    "show list of commands."
    b = event.bot()
    event.reply(",".join(sorted(b.modnames)))

