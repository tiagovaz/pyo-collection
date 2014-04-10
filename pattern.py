#!/usr/bin/python

"""
Flexible pattern using Pattern() function and pure python conditions
"""

from pyo import *

s = Server(audio='jack').boot()

#t = CosTable([(0,0), (100,1), (500,.3), (8191,0)])
#amp = TableRead(t, freq=1, loop=False)
amp = Fader(fadein=.1, fadeout=.1, dur=.1)
sin = Sine(freq=[40, 40.5], mul=amp).out()

beat = 1
count = 1

def pat():
    global beat
    if beat == 1:
        amp.play()
    if beat == 30:
        amp.play()
    if beat == 32:
        beat = 1
    else:
        beat = beat + 1

p = Pattern(pat, .125)
p.play()

s.gui(locals())
