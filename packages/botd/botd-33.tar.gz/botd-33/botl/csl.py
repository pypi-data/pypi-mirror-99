# This file is in the Public Domain.

import atexit
import os
import readline
import sys
import termios

from . import cdir, cfg, cprint, j, op, update
from .evt import Command, Event
from .hdl import Core
from .prs import parse as myparse
from .sel import Select
from .thr import launch

cmds = []
resume = {}

def init(hdl):
    c = Console()
    c.clone(hdl)
    c.start()
    return c

class Shell(Core):

    def dosay(self, channel, txt):
        if not self.stopped:
            print(txt)

class Console(Shell):

    def handle(self, e):
        super().handle(e)
        e.wait()

    def poll(self):
        return Command(input("> "))

    def start(self):
        self.connected.set()
        launch(self.input)
        super().start()

class SelectConsole(Select, Shell):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_fd(sys.stdin)

    def poll(self, fd):
        return Command(input("> "))

class Test(Core):

    def dosay(self, channel, txt):
        if op("v") and not self.stopped:
            print(txt)

def termsetup(fd):
    return termios.tcgetattr(fd)

def termreset():
    if "old" in resume:
        try:
            termios.tcsetattr(resume["fd"], termios.TCSADRAIN, resume["old"])
        except termios.error:
            pass

def termsave():
    try:
        resume["fd"] = sys.stdin.fileno()
        resume["old"] = termsetup(sys.stdin.fileno())
        atexit.register(termreset)
    except termios.error:
        pass

def complete(text, state):
    matches = []
    if text:
        matches = [s for s in cmds if s and s.startswith(text)]
    else:
        matches = cmds[:]
    try:
        return matches[state]
    except IndexError:
        return None

def exec(main):
    termsave()
    try:
        main()
    except KeyboardInterrupt:
        pass
    except PermissionError:
        cprint("you need root privileges")
    finally:
        termreset()

def parse():
    myparse(cfg, " ".join(sys.argv[1:]))
    update(cfg, cfg.sets)
    sd = j(cfg.wd, "store")
    if not os.path.exists(sd):
        cdir(sd)
    return cfg

def setcompleter(commands):
    cmds.extend(commands)
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))
