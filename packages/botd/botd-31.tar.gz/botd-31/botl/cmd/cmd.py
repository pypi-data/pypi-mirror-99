# This file is in the Public Domain.

def cmd(event):
    b = event.bot()
    event.reply(",".join(sorted(b.modnames)))

