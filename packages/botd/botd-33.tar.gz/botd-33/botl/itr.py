# This file is placed in the Public Domain.

import os
import inspect
import pkgutil
import sys

from botl import Object, ObjectList, direct, mods, spl, update
from botl.utl import hasmod

def findcmds(mod):
    cmds = Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                if key not in cmds:
                    cmds[key] = o
    return cmds

def findfuncs(mod):
    funcs = Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                if key not in funcs:
                    funcs[key] = "%s.%s" % (o.__module__, o.__name__)
    return funcs

def findmods(mod):
    mods = Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                if key not in mods:
                    mods[key] = o.__module__
    return mods

def findmodules(pns):
    mods = []
    for mn in findall(pns):
        if mn in mods:
            continue
        mod = direct(mn)
        if findcmds(mod):
            mods.append(mn)
    return mods

def findclasses(mod):
    nms = ObjectList()
    for _key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            t = "%s.%s" % (o.__module__, o.__name__)
            nms.append(o.__name__, t)
    return nms

def findclass(mod):
    mds = ObjectList()
    for key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            mds.append(o.__name__, o.__module__)
    return mds

def findnames(mod):
    tps = Object()
    for _key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, Object):
            t = "%s.%s" % (o.__module__, o.__name__)
            if t not in tps:
                tps[o.__name__.lower()] = t
    return tps

def findall(names):
    for pn in spl(names):
        try:
            mod = direct(pn)
        except ModuleNotFoundError:
            continue
        if "__file__" in dir(mod) and mod.__file__:
            pths = [os.path.dirname(mod.__file__),]
            for m, n, p in pkgutil.iter_modules(pths):
                fqn = "%s.%s" % (pn, n)
                yield fqn
        else:
            p = list(mod.__path__)[0]
            if not os.path.exists(p):
                continue
            for mn in [x[:-3] for x in os.listdir(p) if x.endswith(".py")]:
                fqn = "%s.%s" % (pn, mn)
                yield fqn

def getnames(pkgs):
    res = Object()
    for pkg in spl(pkgs):
        for mod in mods(pkg):
            n = findnames(mod)
            update(res, n)
    return res

def scan(h, mod):
    mn = mod.__name__
    h.pnames[mn.split(".")[-1]] = mn
    update(h.modnames, findmods(mod))
    h.names.update(findnames(mod))

def scandir(o, path, name=""):
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
        scan(o, mod)

def walk(names):
    oo = Object()
    oo.pnames = Object()
    oo.names = ObjectList()
    oo.modnames = Object()
    for mn in findall(names):
        mod = direct(mn)
        oo.pnames[mn.split(".")[-1]] = mn
        update(oo.modnames, findmods(mod))
        oo.names.update(findnames(mod))
    return oo
