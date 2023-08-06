# This file is placed in the Public Domain.

import os
import queue
import socket
import sys
import textwrap
import time
import threading
import  _thread

from . import Cfg, Object, cfg, cprint
from .bus import Bus
from .csl import Shell, op
from .dbs import last
from .evt import Event
from .hdl import Core
from .thr import launch
from .usr import Users
from .utl import debug, getexception, locked

def init(hdl):
    i = IRC()
    i.clone(hdl)
    i.start()
    return i

saylock = _thread.allocate_lock()

class Cfg(Cfg):

    channel = "#botd"
    nick = "botd"
    port = 6667
    server = "localhost"
    realname = "24/7 channel daemon"
    username = "botd"

    def __init__(self):
        super().__init__()
        self.channel = Cfg.channel
        self.nick = Cfg.nick
        self.port = Cfg.port
        self.server = Cfg.server
        self.realname = Cfg.realname
        self.username = Cfg.username

class Event(Event):

    pass

class TextWrap(textwrap.TextWrapper):

    def __init__(self):
        super().__init__()
        self.break_long_words = False
        self.drop_whitespace = False
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 450

class IRC(Core):

    def __init__(self):
        super().__init__()
        self.buffer = []
        self.cc = "!"
        self.cfg = Cfg()
        self.cmds = Object()
        self.channels = []
        self.fsock = None
        self.joined = threading.Event()
        self.sock = None
        self.state = Object()
        self.state.needconnect = False
        self.state.error = ""
        self.state.last = 0
        self.state.lastline = ""
        self.state.nrconnect = 0
        self.state.nrerror = 0
        self.state.nrsend = 0
        self.state.pongcheck = False
        self.threaded = False
        self.users = Users()
        self.zelf = ""
        self.register("error", error)
        self.register("ERROR", self.ERROR)
        self.register("LOG", self.LOG)
        self.register("NOTICE", self.NOTICE)
        self.register("PRIVMSG", self.PRIVMSG)
        self.register("QUIT", self.QUIT)
        self.register("366", self.JOINED)

    def announce(self, txt):
        for channel in self.channels:
            self.say(channel, txt)

    def command(self, cmd, *args):
        if not args:
            self.raw(cmd)
            return
        if len(args) == 1:
            self.raw("%s %s" % (cmd.upper(), args[0]))
            return
        if len(args) == 2:
            self.raw("%s %s :%s" % (cmd.upper(), args[0], " ".join(args[1:])))
            return
        if len(args) >= 3:
            self.raw("%s %s %s :%s" % (cmd.upper(), args[0], args[1], " ".join(args[2:])))
            return

    def connect(self, server, port=6667):
        cprint("connect %s:%s" % (server, port))
        addr = socket.getaddrinfo(server, port, socket.AF_INET)[-1][-1]
        s = socket.create_connection(addr)
        self.cfg.resume = s.fileno()
        os.set_inheritable(self.cfg.resume, os.O_RDWR)
        s.setblocking(True)
        s.settimeout(1200.0)
        self.sock = s
        self.fsock = self.sock.makefile("r")
        return True

    def doconnect(self, server, nick, port=6667):
        while not self.stopped:
            self.state.nrconnect += 1
            try:
                if self.connect(server, port):
                    break
            except OSError:
                pass
            time.sleep(10.0)
        self.connected.set()
        self.logon(server, nick)

    @locked(saylock)
    def dosay(self, channel, txt):
        wrapper = TextWrap()
        txt = str(txt).replace("\n", "")
        for t in wrapper.wrap(txt):
            if not t:
                continue
            self.command("PRIVMSG", channel, t)
            if (time.time() - self.state.last) < 4.0:
                time.sleep(4.0)
            self.state.last = time.time()

    def handle(self, event):
        if event.command in self.cbs:
            self.cbs[event.command](event)

    def joinall(self):
        for channel in self.channels:
            self.command("JOIN", channel)

    def keep(self):
        while not self.stopped:
            time.sleep(60)
            self.state.pongcheck = True
            self.command("PING", self.state.host)
            time.sleep(2.0)
            if self.state.pongcheck:
                 self.reconnect()
                 break
                     
    def logon(self, server, nick):
        self.raw("NICK %s" % nick)
        self.raw("USER %s %s %s :%s" % (self.cfg.username, server, server, self.cfg.realname))

    def parsing(self, txt):
        rawstr = str(txt)
        rawstr = rawstr.replace("\u0001", "")
        rawstr = rawstr.replace("\001", "")
        cprint(txt)
        o = Event()
        o.rawstr = rawstr
        o.orig = repr(self)
        o.command = ""
        o.arguments = []
        arguments = rawstr.split()
        if arguments:
            o.origin = arguments[0]
        else:
            o.origin = self.cfg.server
        if o.origin.startswith(":"):
            o.origin = o.origin[1:]
            if len(arguments) > 1:
                o.command = arguments[1]
                o.type = o.command
            if len(arguments) > 2:
                txtlist = []
                adding = False
                for arg in arguments[2:]:
                    if arg.count(":") <= 1 and arg.startswith(":"):
                        adding = True
                        txtlist.append(arg[1:])
                        continue
                    if adding:
                        txtlist.append(arg)
                    else:
                        o.arguments.append(arg)
                o.txt = " ".join(txtlist)
        else:
            o.command = o.origin
            o.origin = self.cfg.server
        try:
            o.nick, o.origin = o.origin.split("!")
        except ValueError:
            o.nick = ""
        target = ""
        if o.arguments:
            target = o.arguments[-1]
        if target.startswith("#"):
            o.channel = target
        else:
            o.channel = o.nick
        if not o.txt:
            if rawstr[0] == ":":
                rawstr = rawstr[1:]
            o.txt = rawstr.split(":", 1)[-1]
        if not o.txt and len(arguments) == 1:
            o.txt = arguments[1]
        spl = o.txt.split()
        if len(spl) > 1:
            o.args = spl[1:]
        return o

    def poll(self):
        if not self.buffer:
            self.some()
        if not self.buffer:
            return
        e = self.parsing(self.buffer.pop(0))
        cmd = e.command
        if cmd == "PING":
            self.state.pongcheck = True
            self.command("PONG", e.txt or "")
        elif cmd == "PONG":
            self.state.pongcheck = False
        if cmd == "001":
            self.state.needconnect = False
            if "servermodes" in dir(self.cfg):
                self.raw("MODE %s %s" % (self.cfg.nick, self.cfg.servermodes))
            self.zelf = e.args[-1]
            self.joinall()
        elif cmd == "002":
            self.state.host = e.args[2][:-1]
        elif cmd == "366":
            self.joined.set()
        elif cmd == "433":
            nick = self.cfg.nick + "_"
            self.cfg.nick = nick
            self.raw("NICK %s" % self.cfg.nick)
        return e

    def raw(self, txt):
        txt = txt.rstrip()
        if not txt.endswith("\r\n"):
            txt += "\r\n"
        txt = txt[:512]
        cprint(txt.rstrip())
        txt = bytes(txt, "utf-8")
        try:
            self.sock.send(txt)
        except (OSError, ConnectionResetError) as ex:
            e = Event()
            e.error = getexception()
            self.ERROR(e)
        self.state.last = time.time()
        self.state.nrsend += 1

    def reconnect(self):
        self.stop()
        time.sleep(5.0)
        self.stopped = False
        self.start()

    def say(self, channel, txt):
        if not self.stopped:
            self.outqueue.put_nowait((channel, txt))

    def some(self):
        inbytes = self.sock.recv(512)
        txt = str(inbytes, "utf-8")
        if txt == "":
            raise ConnectionResetError
        self.state.lastline += txt
        splitted = self.state.lastline.split("\r\n")
        for s in splitted[:-1]:
            self.buffer.append(s)
        self.state.lastline = splitted[-1]

    def start(self):
        last(self.cfg)
        self.channels.append(self.cfg.channel)
        super().start()
        self.stopped = False
        self.doconnect(self.cfg.server, self.cfg.nick, int(self.cfg.port) or 6667)
        launch(self.output)
        launch(self.input)
        launch(self.keep)
        self.joined.wait()

    def stop(self):
        self.stopped = True
        self.outqueue.put((None, None))
        if self.sock:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        super().stop()
        
    def ERROR(self, event):
        self.state.nrerror += 1
        self.state.error = event.error
        cprint(event.error)
        if "kill" not in event.txt.lower():
            self.reconnect()
        
    def JOINED(self, event):
        self.joined.set()

    def KILL(self, event):
        print(event)

    def LOG(self, event):
        pass

    def NOTICE(self, event):
        if event.txt.startswith("VERSION"):
            txt = "\001VERSION %s %s - %s\001" % (self.cfg.nick.upper(), self.cfg.version or 1, self.cfg.username)
            self.command("NOTICE", event.channel, txt)

    def PRIVMSG(self, pevent):
        if pevent.txt.startswith("DCC CHAT"):
            if not self.users.allowed(pevent.origin, "USER"):
                return
            try:
                dcc = DCC()
                dcc.clone(self)
                dcc.encoding = "utf-8"
                launch(dcc.connect, pevent)
                return
            except ConnectionError as ex:
                return
        if pevent.txt and pevent.txt[0] == self.cc:
            if not self.users.allowed(pevent.origin, "USER"):
                return
            pevent.type = "cmd"
            pevent.txt = pevent.txt[1:]
            super().dispatch(pevent)

    def QUIT(self, event):
        if event.orig and event.orig in self.zelf:
            self.reconnect()

class DCC(Shell):

    def __init__(self):
        super().__init__()
        self.sock = None
        self.fsock = None
        self.encoding = "utf-8"
        self.origin = ""
        self.stopped = False

    def raw(self, txt):
        self.fsock.write(str(txt).rstrip())
        self.fsock.write("\n")
        self.fsock.flush()

    def announce(self, txt):
        pass

    def connect(self, dccevent):
        if self.stopped:
            return
        dccevent.parse()
        arguments = dccevent.old.txt.split()
        addr = arguments[3]
        port = int(arguments[4])
        if ':' in addr:
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((addr, port))
        except ConnectionRefusedError:
            self.connected.set()
            return
        s.setblocking(1)
        os.set_inheritable(s.fileno(), os.O_RDWR)
        self.sock = s
        self.fsock = self.sock.makefile("rw")
        self.raw('Welcome %s' % dccevent.origin)
        self.origin = dccevent.origin
        self.connected.set()
        launch(self.input)
        super().start()

    def poll(self):
        e = Event()
        e.type = "cmd"
        e.channel = self.origin
        e.origin = self.origin or "root@dcc"
        e.orig = repr(self)
        txt = self.fsock.readline()
        e.txt = txt.rstrip()
        e.sock = self.sock
        e.fsock = self.fsock
        return e

    def say(self, channel, txt):
        if not self.stopped:
            self.raw(txt)

def error(hdl, obj):
    cprint(event.error)
