#!/usr/bin/python

"""
Flexible pattern using Pattern() function and pure python conditions
"""

from pyo import *

s = Server(audio='jack').boot()

class MySine:
    def __init__(self, freq_factor=.99):
        self.amp = Fader(fadein=.01, fadeout=.01, dur=.25).stop()
        self.sin = Sine(freq=400*freq_factor, mul=self.amp).out()

    def play(self):
        self.amp.play()

sin = MySine(.5)
sin2 = MySine(.3)

class MyPattern:
    def __init__(self, instrument, time=.25, beats=32, beats_to_play=[1, 8, 10, 12, 18, 24, 30]):
        self.p = Pattern(self.pat, time).stop()
        self.beats = beats
        self.current_beat = 1
        self.instrument = instrument
        self.beats_to_play = beats_to_play

    def pat(self):
        if self.current_beat in self.beats_to_play:
            self.instrument.play()
        if self.current_beat == self.beats:
            self.current_beat = 1
        self.current_beat += 1

    def play(self):
        self.p.play()

    def stop(self):
        self.p.stop()


p = MyPattern(sin, beats_to_play=[1, 32])
p.play()

s.gui(locals())
