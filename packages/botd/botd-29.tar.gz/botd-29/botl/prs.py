# This file is placed in the Public Domain.

from . import Default, Object, update
from .utl import day, time

year_formats = [
    "%b %H:%M",
    "%b %H:%M:%S",
    "%a %H:%M %Y",
    "%a %H:%M",
    "%a %H:%M:%S",
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d-%m",
    "%m-%d",
    "%Y-%m-%d %H:%M:%S",
    "%d-%m-%Y %H:%M:%S",
    "%d-%m %H:%M:%S",
    "%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%d-%m-%Y %H:%M",
    "%d-%m %H:%M",
    "%m-%d %H:%M",
    "%H:%M:%S",
    "%H:%M"
]

class Token(Object):

    def __init__(self, txt):
        super().__init__()
        self.txt = txt

class Option(Default):

    def __init__(self, txt):
        super().__init__()
        if txt.startswith("--"):
            self.opt = txt[2:]
        if txt.startswith("-"):
            self.opt = txt[1:]

class Getter(Object):

    def __init__(self, txt):
        super().__init__()
        try:
            pre, post = txt.split("==")
        except ValueError:
            pre = post = ""
        if pre:
            self[pre] = post

class Setter(Object):

    def __init__(self, txt):
        super().__init__()
        try:
            pre, post = txt.split("=")
        except ValueError:
            pre = post = ""
        if pre:
            self[pre] = post

class Skip(Object):

    def __init__(self, txt):
        super().__init__()
        pre = ""
        if txt.endswith("-"):
            try:
                pre, _post = txt.split("=")
            except ValueError:
                try:
                    pre, _post = txt.split("==")
                except ValueError:
                    pre = txt
        if pre:
            self[pre] = True

class Timed(Object):

    def __init__(self, txt):
        super().__init__()
        v = 0
        vv = 0
        try:
            pre, post = txt.split("-")
            v = parse_time(pre)
            vv = parse_time(post)
        except ValueError:
            pass
        if not v or not vv:
            try:
                vv = parse_time(txt)
            except ValueError:
                vv = 0
            v = 0
        if v:
            self["from"] = time.time() - v
        if vv:
            self["to"] = time.time() - vv

def parse(o, txt):
    o.old = o.old or Default()
    o.old.txt = txt
    o.gets = o.gets or Default()
    o.opts = o.opts or Default()
    o.timed = o.timed or []
    o.index = o.index or None
    o.sets = o.sets or Default()
    o.skip = o.skip or Default()
    args = []
    for token in [Token(txt) for txt in txt.split()]:
        s = Skip(token.txt)
        if s:
            update(o.skip, s)
            token.txt = token.txt[:-1]
        t = Timed(token.txt)
        if t:
            update(o.timed, t)
            continue
        g = Getter(token.txt)
        if g:
            update(o.gets, g)
            continue
        s = Setter(token.txt)
        if s:
            update(o.sets, s)
            continue
        opt = Option(token.txt)
        if opt:
            try:
                o.index = int(opt.opt)
                continue
            except ValueError:
                pass
            if len(opt.opt) > 1:
                for op in opt.opt:
                    o.opts[op] = True
            else:
                o.opts[opt.opt] = True
            continue
        args.append(token.txt)
    if not args:
        o.args = []
        o.cmd = ""
        o.rest = ""
        o.txt = ""
        return o
    o.cmd = args[0]
    o.args = args[1:]
    o.txt = " ".join(args)
    o.rest = " ".join(args[1:])
    return o

def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    sec = nsec - minutes*minute
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt
    if hours:
        txt += "%sh" % hours
    if nrdays and short and txt:
        return txt
    if minutes:
        txt += "%sm" % minutes
    if hours and short and txt:
        return txt
    if sec == 0:
        txt += "0s"
    else:
        txt += "%ss" % int(sec)
    txt = txt.strip()
    return txt

def parse_time(daystring):
    line = ""
    daystr = str(daystring)
    for word in daystr.split():
        if "-" in word:
            line += word + " "
        elif ":" in word:
            line += word
    if "-" not in line:
        line = day() + " " + line
    for f in year_formats:
        try:
            t = time.mktime(time.strptime(line, f))
            return t
        except ValueError:
            pass

def parse_ymd(daystr):
    valstr = ""
    val = 0
    total = 0
    for c in daystr:
        try:
            vv = int(valstr)
        except ValueError:
            vv = 0
        if c == "y":
            val = vv * 3600*24*365
        if c == "w":
            val = vv * 3600*24*7
        elif c == "d":
            val = vv * 3600*24
        elif c == "h":
            val = vv * 3600
        elif c == "m":
            val = vv * 60
        else:
            valstr += c
        total += val
    return total
