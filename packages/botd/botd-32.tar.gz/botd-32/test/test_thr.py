# This file is placed in the Public Domain.

import random
import unittest

from botl import cfg
from botl.evt import Command
from botl.thr import launch

from test.prm import param
from test.run import h

events = []

class Test_Threaded(unittest.TestCase):

    def setUp(self):
        h.start()
        
    def tearDown(self):
        h.stop()

    def test_thrs(self):
        thrs = []
        for x in range(cfg.index or 1):
            thr = launch(exec)
            thrs.append(thr)
        for thr in thrs:
            thr.join()
        consume()

def consume():
    fixed = []
    res = []
    for e in events:
        e.wait()
        fixed.append(e)
    for f in fixed:
        try:
            events.remove(f)
        except ValueError:
            continue
    return res

def exec():
    l = list(h.modnames)
    random.shuffle(l)
    for cmd in l:
        for ex in getattr(param, cmd, [""]):
            txt = cmd + " " + ex
            e = Command(txt)
            h.put(e)
            events.append(e)
