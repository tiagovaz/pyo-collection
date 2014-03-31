#!/usr/bin/python

"""
Simple beat pattern using Beat() function
"""

from pyo import *

s = Server(audio='jack').boot()
s.start()

t = CosTable([(0,0), (100,1), (500,.3), (8191,0)])

beat = Beat(time=.5, taps=16, w1=100, w2=0, w3=0, poly=1).play()
tr = TrigEnv(beat, table=t, dur=beat['dur'], mul=beat['amp'])
a = Sine(freq=[40, 40.5], mul=tr*0.5)

beat2 = Beat(time=.125, taps=16, w1=0, w2=100, w3=0, poly=1).play()
tr2 = TrigEnv(beat2, table=t, dur=beat2['dur'], mul=beat2['amp'])
b = Sine(freq=[40, 40.5], mul=tr2*0.3)

m = Mix([a, b], voices=2).out()

s.gui(locals())
