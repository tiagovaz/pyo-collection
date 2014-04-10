#!/usr/bin/env python
# encoding: utf-8
from pyo import *
import random

s = Server(audio='jack', sr=44100, nchnls=2, buffersize=512, duplex=1).boot()

POLY = 4

env = Adsr(dur=0.5, mul=[.2]*POLY) # 4 Adsr...
syn = Sine(mul=env).out() # ... donc 4 sinus

which = 0
def note():
    global which
    freq = random.uniform(500, 1000)
    syn[which].setFreq(freq)
    env[which].play()
    which = (which + 1) % POLY # alterne les synths

pat = Pattern(note, 0.2).play()

s.gui(locals())
