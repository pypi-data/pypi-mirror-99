# This file is placed in the Public Domain.

import os
import queue
import socket
import sys
import threading
import time
import _thread

from . import Object, ObjectList, cfg, cprint, direct, format, locked, j, spl, update
from .bus import Bus
from .evt import Command, Event
from .itr import findcmds
from .itr import scan as iscan
from .thr import launch
from .utl import getexception, hasmod

loadlock = _thread.allocate_lock()

class Handler(Object):

    table = Object()
    pnames = Object()
    modnames = Object()
    names = ObjectList()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.cbs = Object()
        self.cmds = Object()
        self.queue = queue.Queue()
        self.inqueue = queue.Queue()
        self.outqueue = queue.Queue()
        self.started = False
        self.stopped = False
        self.connected = threading.Event()

    def add(self, cmd, func):
        self.cmds[cmd] = func
        Handler.modnames[cmd] = func.__module__

    def announce(self, txt):
        pass

    def clone(self, hdl):
        update(self.cmds, hdl.cmds)

    def direct(self, txt):
        pass

    def dosay(self, channel, txt):
        pass

    def dispatch(self, event):
        if event.type and event.type in self.cbs:
            self.cbs[event.type](self, event)

    def getcmd(self, cmd):
        if cmd not in self.cmds:
            mn = getattr(Handler.modnames, cmd, None)
            if mn:
                self.load(mn)
        return getattr(self.cmds, cmd, None)

    def getmod(self, mn):
        if mn in Handler.table:
            return Handler.table[mn]

    def getnames(self, nm):
        return getattr(Handler.names, nm, [nm,])

    def handler(self):
        self.running = True
        while not self.stopped:
            e = self.queue.get()
            if not e:
                break
            if not e.orig:
                e.orig = repr(self)
            thr = launch(self.dispatch, e)
            e.thrs.append(thr)

    def handle(self, e):
        self.put(e)

    def init(self, mns):
        thrs = []
        result = []
        for mn in spl(mns):
            mn = getattr(Handler.pnames, mn, mn)
            mod = self.load(mn)
            if mod and "init" in dir(mod):
                thr = launch(mod.init, self)
                thrs.append(thr)
        for thr in thrs:
            result.append(thr.join())
        return result

    def input(self):
        self.connected.wait()
        while not self.stopped:
            try:
                e = self.poll()
            except (ConnectionResetError, OSError, socket.error):
                e = Event()
                e.type = "error"
                e.error = getexception()
                self.handle(e)
                break
            if not e:
                break
            if not e.orig:
                e.orig = repr(self)
            self.handle(e)
            time.sleep(0.01)

    @locked(loadlock)
    def load(self, mn):
        if not "." in mn:
            return None
        mnn = getattr(Handler.pnames, mn, mn)
        mod = direct(mnn)
        cmds = findcmds(mod)
        update(self.cmds, cmds)
        Handler.table[mn] = mod
        return mod

    def once(self, txt):
        self.connected.set()
        self.stopped = False
        self.running = True
        c = Command(txt)
        c.orig = repr(self)
        cmd(self, c)
        c.wait()

    def output(self, once=False):
        while not self.stopped:
            channel, txt = self.outqueue.get()
            if channel is None:
                break
            if txt:
                self.dosay(channel, txt)
            if once:
                break
            time.sleep(0.01)

    def poll(self):
        pass

    def put(self, e):
        self.queue.put_nowait(e)

    def register(self, name, callback):
        self.cbs[name] = callback

    def resume(self):
        pass

    def say(self, channel, txt):
        if not self.stopped:
            self.dosay(channel, txt)

    def scan(o, path, name=""):
        if not os.path.exists(path):
            return
        if not name:
            name = path.split(os.sep)[-1]
        r = os.path.dirname(path)
        if r not in sys.path:
            sys.path.insert(0, r)
        for mn in [x[:-3] for x in os.listdir(path)
                   if x and x.endswith(".py")
                   and not x.startswith("__")
                   and not x == "setup.py"]:
            fqn = "%s.%s" % (name, mn)
            if not hasmod(fqn):
                continue
            mod = o.load(fqn)
            iscan(o, mod)

    def tbl(self, tbl):
        Handler.names.update(tbl["names"])
        update(Handler.modnames, tbl["modnames"])
        update(Handler.pnames, tbl["pnames"])

    def start(self):
        self.stopped = False
        launch(self.handler)
        return self

    def stop(self):
        self.stopped = True
        self.started = False
        self.queue.put(None)

    def wait(self, timeout=5.0):
        while not self.stopped:
            time.sleep(timeout)

class Core(Handler):

    def __init__(self):
        super().__init__()
        self.register("cmd", cmd)
        self.register("error", error)
        Bus.add(self)

def cmd(hdl, obj):
    obj.parse()
    f = hdl.getcmd(obj.cmd)
    res = None
    if f:
        res = f(obj)
        obj.show()
    obj.ready()
    return res

def error(hdl, obj):
    cprint(str(obj))
        