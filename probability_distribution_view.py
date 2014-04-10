#!/usr/bin/env python
# encoding: utf-8
from pyo import *
from random import *

s = Server(audio='jack', sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

table = DataTable(size=128)
table.view()

def new(t=3.2):
    l = [int(weibullvariate(0.5, t) * 127) for i in range(4000)]
    l2 = []
    for i in range(128):
        l2.append(l.count(i))
    table.replace(l2)
    table.normalize()
    table.refreshView()

val = 0
def change():
    global val
    new(val+0.25)
    val = (val + 0.1) % 10

pat = Pattern(change, .2).play()

s.gui(locals())
