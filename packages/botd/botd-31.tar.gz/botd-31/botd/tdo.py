# This file is in the Public Domain.

from botl import Object, save
from botl.dbs import find

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def dne(event):
    if not event.args:
        return
    selector = {"txt": event.args[0]}
    for fn, o in find("botd.tdo.Todo", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break

def tdo(event):
    if not event.rest:
        return
    o = Todo()
    o.txt = event.rest
    save(o)
    event.reply("ok")
