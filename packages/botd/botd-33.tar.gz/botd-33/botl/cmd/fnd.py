# This file is placed in the Public Domain.

import os
import time

from botl import cfg, format, keys, op
from botl.dbs import find, listfiles
from botl.prs import elapsed
from botl.utl import fntime

def fnd(event):
    if not event.args:
        fls = listfiles(cfg.wd)
        if fls:
            event.reply("|".join([x.split(".")[-1].lower() for x in fls]))
        return
    name = event.args[0]
    b = event.bot()
    t = b.getnames(name)
    nr = -1
    for otype in t:
        for fn, o in find(otype, event.gets, event.index, event.timed):
            nr += 1
            txt = "%s %s" % (str(nr), format(o, False, event.skip, keys(o)))
            if "t" in event.opts:
                txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
            event.reply(txt)
