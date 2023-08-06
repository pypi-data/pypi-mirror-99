# This file is in the Public Domain.

"administrator commands."

import os
import threading
import time

from botl import Object, cfg, edit, format, getname, save, starttime, update
from botl.bus import Bus
from botl.prs import elapsed
from botl.itr import findmodules

def flt(event):
    "show list of running bots."
    try:
        event.reply(str(Bus.objs[event.index]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(" | ".join([getname(o) for o in Bus.objs]))

def hlp(event):
    "display help string of command."
    if not event.args:
        return
    cmd = event.args[0]
    b = event.bot()
    c = b.getcmd(cmd)
    event.reply(c.__doc__)

def krn(event):
    "edit/show basic configuration."
    if not event.sets:
        event.reply(format(cfg, skip=["opts", "sets", "old", "res"]))
        return
    edit(cfg, event.sets)
    save(cfg)
    event.reply("ok")

def thr(event):
    "list of running threads."
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        o = Object()
        update(o, thr)
        if getattr(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        thrname = thr.getName()
        if not thrname:
            continue
        if thrname:
            result.append((up, thrname))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s %s" % (txt, elapsed(up)))
    if res:
        event.reply(" | ".join(res))

def upt(event):
    "display uptime."
    event.reply("uptime is %s" % elapsed(time.time()-starttime))
