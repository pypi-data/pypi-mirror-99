# This file is placed in the Public Domain.

import datetime
import getpass
import inspect
import json
import os
import pwd
import random
import re
import sys
import time
import traceback
import importlib
import importlib.util

import urllib
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

debug = False

timestrings = [
    "%a, %d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S",
    "%a, %d %b %Y %H:%M:%S",
    "%d %b %a %H:%M:%S %Y %Z",
    "%d %b %a %H:%M:%S %Y %z",
    "%a %d %b %H:%M:%S %Y %z",
    "%a %b %d %H:%M:%S %Y",
    "%d %b %Y %H:%M:%S",
    "%a %b %d %H:%M:%S %Y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dt%H:%M:%S+00:00",
    "%a, %d %b %Y %H:%M:%S +0000",
    "%d %b %Y %H:%M:%S +0000",
    "%d, %b %Y %H:%M:%S +0000"
]

class ENOCLASS(Exception):

    pass

def day():
    return str(datetime.datetime.today()).split()[0]

def direct(name, pname=''):
    return importlib.import_module(name, pname)

def e(p):
    return os.path.expanduser(p)

def filetime(timestamp):
    s = str(datetime.datetime.fromtimestamp(timestamp))
    return s.replace(" ", os.sep) + "." + str(random.randint(111111, 999999))

def fntime(daystr):
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    try:
        datestr, rest = datestr.rsplit(".", 1)
    except ValueError:
        rest = ""
    try:
        t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
        if rest:
            t += float("." + rest)
    except ValueError:
        t = 0
    return t

def getargs(f):
    spec = inspect.signature(f)
    return spec.parameters

def getcls(fullname):
    try:
        modname, clsname = fullname.rsplit(".", 1)
    except Exception as ex:
        raise ENOCLASS(fullname) from ex
    mod = importlib.import_module(modname)
    return getattr(mod, clsname)

def getexception(txt="", sep=" "):
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = []
    for elem in trace:
        if "python3" in elem[0] or "<frozen" in elem[0]:
            continue
        res = []
        for x in elem[0].split(os.sep)[::-1]:
            res.append(x)
            if x in ["ok"]:
                break
        result.append("%s:%s" % (os.sep.join(res[::-1]), elem[1]))
    res = "%s %s: %s %s" % (sep.join(result), exctype, excvalue, str(txt))
    del trace
    return res

def gettinyurl(url):
    if debug:
        return []
    postarray = [
        ('submit', 'submit'),
        ('url', url),
        ]
    postdata = urlencode(postarray, quote_via=quote_plus)
    req = Request('http://tinyurl.com/create.php', data=bytes(postdata, "UTF-8"))
    req.add_header('User-agent', useragent(url))
    for txt in urlopen(req).readlines():
        line = txt.decode("UTF-8").strip()
        i = re.search('data-clipboard-text="(.*?)"', line, re.M)
        if i:
            return i.groups()
    return []

def geturl(url):
    if debug:
        return
    url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
    req = urllib.request.Request(url)
    req.add_header('User-agent', useragent(url))
    response = urllib.request.urlopen(req)
    response.data = response.read()
    return response

def hasmod(fqn):
    try:
        spec = importlib.util.find_spec(fqn)
        if spec:
            return True
    except (ValueError, ModuleNotFoundError):
        pass
    return False

def hook(hfn):
    from . import load
    if hfn.count(os.sep) > 3:
        oname = hfn.split(os.sep)[-4:]
    else:
        oname = hfn.split(os.sep)
    cname = oname[0]
    fn = os.sep.join(oname)
    cls = getcls(cname)
    o = cls()
    load(o, fn)
    return o

def j(*args):
    return os.path.join(*args)

def locked2(l):
    def lockeddec(func, *args, **kwargs):
        l.acquire()
        res = None
        try:
            res = func(*args, **kwargs)
        finally:
            l.release()
        lockeddec.__wrapped__ = func
        return res
    return lockeddec

def locked(l):
    def lockeddec(func, *args, **kwargs):
        def lockedfunc(*args, **kwargs):
            l.acquire()
            res = None
            try:
                res = func(*args, **kwargs)
            finally:
                l.release()
            return res
        lockedfunc.__wrapped__ = func
        return lockedfunc
    return lockeddec

def opcheck(ops, cfg):
    for o in ops:
        if o in cfg.opts:
            return True
    return False

def privileges(name=None):
    if os.getuid() != 0:
        return
    if name is None:
        try:
            name = getpass.getuser()
        except KeyError:
            pass
    try:
        pwnam = pwd.getpwnam(name)
    except KeyError:
        return False
    os.setgroups([])
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)
    old_umask = os.umask(0o22)
    return True

def root():
    if os.geteuid() != 0:
        return False
    return True

def striphtml(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def tojson(d):
    return json.dumps(d, indent=4, sort_keys=True)

def totime(daystr):
    daystr = daystr.strip()
    if "," in daystr:
        daystr = " ".join(daystr.split(None)[1:7])
    elif "(" in daystr:
        daystr = " ".join(daystr.split(None)[:-1])
    else:
        try:
            d, h = daystr.split("T")
            h = h[:7]
            daystr = " ".join([d, h])
        except (ValueError, IndexError):
            pass
    res = 0
    for tstring in timestrings:
        try:
            res = time.mktime(time.strptime(daystr, tstring))
            break
        except ValueError:
            try:
                res = time.mktime(time.strptime(" ".join(daystr.split()[:-1]), tstring))
            except ValueError:
                pass
        if res:
            break
    return res

def unescape(text):
    import html.parser
    txt = re.sub(r"\s+", " ", text)
    return html.unescape(txt)

def useragent(txt):
    return 'Mozilla/5.0 (X11; Linux x86_64) ' + txt

def xdir(o, skip=None):
    res = []
    for k in dir(o):
        if skip is not None and skip in k:
            continue
        res.append(k)
    return res
