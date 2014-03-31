#!/usr/bin/env python
# encoding: utf-8

"""
Copyright 2014 Tiago Bortoletto Vaz <tiago@debian.org>

Glitches is a music composition using Python and Pyo.

Glitches is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Glitches is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Glitches.  If not, see <http://www.gnu.org/licenses/>.
"""

### !!this code is a work in progress!!  ###

from pyo import *
import random

# TODO: refactore to use score events instead of delay/dur strategy
class Instrument:
    def __init__(self):
        pass

    def out(self, delay=0, dur=0):
        self.play(delay=delay, dur=dur)
        self.outsig.out(0, 1, delay=delay, dur=dur)
        return self

    def sig(self):
        return self.outsig

class Sparks:
    def __init__(self, mul=1):
        self.env = LinTable([(0, 0.0000), (0, 1.0000), (2078, 1.0000), (2113, 0.2448), (8174, 0.2448), (8192, 0.0000)])
        self.dens = Expseg([(0, 0), (60, 100)], exp=10).stop()
        self.middur = Expseg([(0, 0.25), (60, 0.05)], inverse=False, exp=6).stop()
        self.trig = Cloud(density=self.dens, poly=2).stop()
        self.dur = TrigRand(self.trig, min=self.middur * 0.5, max=self.middur * 1.5).stop()
        self.amp = TrigEnv(self.trig, self.env, dur=self.dur, mul=0.02).stop()
        self.lff = Sine(.1).range(4000, 5000).stop()
        self.sin = SineLoop(freq=self.lff, feedback=0.4, mul=self.amp * mul).stop()
        self.fade = Fader(fadein=.1, fadeout=.1).stop()
        self.outsig = Mix(self.sin, voices=2, mul=self.fade).stop()

    def play(self):
        print "bli"
        self.dens.play()
        self.middur.play()
        self.trig.play()
        self.dur.play()
        self.amp.play()
        self.lff.play()
        self.sin.play()
        self.fade.play()
        self.outsig.out()

    def tail(self):
        self.fade.stop()

    def stop(self):
        self.dens.stop()
        self.middur.stop()
        self.trig.stop()
        self.dur.stop()
        self.sin.stop()
        self.amp.stop()
        self.lff.stop()
        self.outsig.stop()

class Bass(Instrument):
    def __init__(self, mul=1):
        self.t = LinTable([(0,0.0000),(35,0.9896),(4290,0.6528),(5932,0.2280),(7732,0.1503),(8191,0.0000)])
        self.t.graph()
#        t2 = LinTable[(0,0.0000),(0,0.6995),(494,0.3575),(2701,0.0622),(7909,0.0155),(8191,0.0000)] # glitch
#        t3 = LinTable[(0,0.0000),(0,0.3161),(512,0.1762),(8191,0.0000)] # glitch2
#        t4 = LinTable([(0,0.5181),(0,0.2021),(759,0.2124),(3725,0.1813),(5985,0.0777),(8191,0.0000)]) # glitch3
        self.amp = TableRead(self.t, freq=.1, loop=True).stop()
        self.sin = SineLoop(freq=[24, 24.5], feedback=.05, mul=self.amp).stop()
        self.delay = Delay(self.sin, delay=[0.01, 0.038, 0.72], feedback=0, mul=[1, .78, .29]).stop()
        self.outsig = Mix(self.delay, voices=2, mul=mul).stop()

    def play(self, delay=0, dur=0):
        self.amp.play(delay=delay, dur=dur)
        self.sin.play(delay=delay, dur=dur)
        self.delay.play(delay=delay, dur=dur)
        self.outsig.play(delay=delay, dur=dur)

class Background():
    def __init__(self, freq=1000, q=2, mul=1):
        self.gamp = Expseg([(0, 0), (20, 1), (20.05, 0)], exp=4, mul=mul)  # global amp
        self.lff = Lorenz(0.1, 0.7).range(200, 5000).stop()  # freq control
        self.lfc = Lorenz(0.05, 0.7).range(0.2, 0.5).stop()  # feedback control
        self.gen = SineLoop(freq=self.lff, feedback=self.lfc, mul=0.01).stop()
        self.fade = Fader(fadein=.1, fadeout=.1).stop()
        self.bpfilter = ButBP(self.gen, freq=freq, q=q, mul=self.gamp).stop()
        self.outsig = Mix(self.bpfilter, mul=self.fade).stop()

    def play(self):
        self.gamp.play()
        self.lff.play()
        self.lfc.play()
        self.gen.play()
        self.fade.play()
        self.bpfilter.play()
        self.outsig.out()

    def tail(self):
        self.fade.stop()

    def stop(self):
        self.gamp.stop()
        self.lff.stop()
        self.lfc.stop()
        self.gen.stop()
        self.fade.stop()
        self.bpfilter.stop()
        self.outsig.stop()

class Rumble(Instrument):
    def __init__(self, mul=1):
        self.fade = Fader(fadein=10, fadeout=0.001).stop()
        self.noise = BrownNoise(Randi(min=0.05, max=0.2, freq=[.1, .15])).stop()
        self.lp = ButLP(self.noise, 80, mul=mul).stop()
        self.deg = Degrade(self.lp, bitdepth=5).stop()
        self.rez = Reson(self.deg, freq=[130, 200], q=10, mul=3).stop()
        self.outsig = Mix([self.lp + self.rez], voices=2, mul=self.fade).stop()

    def play(self):
        self.fade.play()
        self.noise.play()
        self.lp.play()
        self.deg.play()
        self.rez.play()
        self.outsig.out()

    def tail(self):
        self.fade.stop()

    def stop(self):
        self.noise.stop()
        self.lp.stop()
        self.deg.stop()
        self.rez.stop()
        self.outsig.stop()

class RythmFou(Instrument):
    def __init__(self, pitch=1177.6, beat_freq=4, fadein=100, mul=1):
        self.t = LinTable([(0,0.0000),(0,0.8187),(1271,0.7358),(1412,0.6788),(2489,0.5907),(3584,0.4093),(4731,0.2124),(4802,0.0881),(4802,0.1140),(5526,0.1036),(6179,0.0829),(6532,0.0622),(6673,0.0000),(7150,0.0000),(8191,0.0000)])
        self.amp = TableRead(table=self.t, freq=beat_freq, loop=True, mul=.3*mul).stop()
        self.sin = SineLoop(freq=[45.8, pitch], feedback=.0885, mul=self.amp).stop()
        self.sin.ctrl()
        self.delay = Delay(self.sin, delay=[0.00371, 0.00190, 0.00131], feedback=0.1692, mul=[1.8, 0.4, 0.086]).stop()
        self.gamp = Fader(fadein=fadein, fadeout=5, dur=0).stop()
        self.outsig = Mix(self.delay, voices=2, mul=self.gamp)

    def play(self, delay, dur):
        self.amp.play(delay=delay, dur=dur)
        self.gamp.play(delay=delay, dur=dur)
        self.sin.play(delay=delay, dur=dur)
        self.delay.play(delay=delay, dur=dur)

class Rhythm(Instrument):
    def __init__(self, freq=2, mul=1):
        self.lf = Sine(random.uniform(.02, .05)).range(.3, .8).stop()
        self.v1 = SineLoop(freq=freq, feedback=self.lf, mul=0.02).stop()
        self.v2 = SineLoop(freq=freq, feedback=self.lf * 0.95, mul=0.02).stop()
        self.outsig = Mix([self.v1, self.v2], voices=2, mul=mul)

    def play(self, delay=0, dur=0):
        self.lf.play(delay=delay, dur=dur)
        self.v1.play(delay=delay, dur=dur)
        self.v2.play(delay=delay, dur=dur)

class DarkBackground(Instrument):
    def __init__(self, fadein=100, p1=.2054, p2=[.3966, .3933], chaos1=.4038, chaos2=.0769, feedback=.5, mul=.5):
        self.r1 = Rossler(pitch=p1, chaos=chaos1, stereo=True, mul=mul, add=.2).stop()
        self.r2 = Rossler(pitch=p2, chaos=chaos2, mul=self.r1*.8).stop()
        self.amp = Fader(fadein=fadein, fadeout=5, dur=0).stop()
        self.outsig = Delay(self.r2, feedback=feedback, mul=self.amp)

    def play(self, delay=0, dur=0):
        self.r1.play(delay=delay, dur=dur)
        self.r2.play(delay=delay, dur=dur)
        self.amp.play(delay=delay, dur=dur)


s = Server(audio='jack', sr=44100, nchnls=2, buffersize=512, duplex=1).boot()
# s.startoffset = 60

# Sparks
sparks = Sparks(mul=.3)

# Rumble
rumble = Rumble(mul=1)

# Background
back1 = Background(freq=400, q=4, mul=3)
back2 = Background(freq=700, q=4, mul=3)
back3 = Background(freq=2700, q=4, mul=3)

# Rythm
ryth1 = Rhythm(freq=.05, mul=.05).out(delay=70, dur=0)
ryth2 = RythmFou(mul=.1, fadein=10, beat_freq=5).out(delay=60, dur=10)
ryth3 = RythmFou(mul=.02, pitch=1200, fadein=1, beat_freq=10).out(delay=90, dur=0)
ryth4 = RythmFou(mul=.01, pitch=632, fadein=5, beat_freq=5).out(delay=95, dur=0)
ryth5 = RythmFou(mul=.03, pitch=590, fadein=.01, beat_freq=5).out(delay=110, dur=0)

# Bass background
sd1 = Sine([36.71, 36], mul=0.1).out(delay=70, dur=0)
sd2 = Sine([72, 73], mul=0.025).out(delay=70, dur=0)
sd3 = Sine([144, 144.2], mul=0.025).out(delay=90, dur=0)
darkback = DarkBackground(mul=.2).out(delay=80, dur=0)
darkback2 = DarkBackground(p2=[.203, .116], chaos1=.39, mul=.5).out(delay=70, dur=0)

# Bass
bass = Bass(mul=.7).out(delay=90, dur=0)
# bass2 = Bass(mul=.5).out(delay=110, dur=0)
# bass3 = Bass(mul=.5).out(delay=120, dur=0)

# Random high freqs
env2 = LinTable([(0, 0.0000), (0, 1.0000), (1694, 1.0000), (1694, 0.0000), (8192, 0.0000)])
rnddur = RandDur(min=[1, 1, 1, 1], max=4)
tenv2 = Change(rnddur)
amp2 = TrigEnv(tenv2, env2, rnddur, mul=0.001)
fr = TrigRand(tenv2, min=7000, max=12000)
syns = Sine(freq=fr, mul=amp2*.5).out(delay=100, dur=0)

### Global time ###
GlitchesSec = 10

### Master counter ###
master = Metro(GlitchesSec).play()
count = Counter(master, min=0, max=100)

#### SCORE ####
def event_0():
    rumble.play()

def event_1():
    sparks.play()

def event_2():
    pass

def event_3():
    pass

def event_4():
    pass

def event_5():
    back1.play()
    back2.play()
    back3.play()

def event_6():
    pass

def event_7():
    sparks.tail()
    back1.tail()
    back2.tail()
    back3.tail()
    rumble.tail()

def event_8():
    back1.stop()
    back2.stop()
    back3.stop()
    rumble.stop()
    sparks.stop()

def event_9():
    pass

def event_10():
    pass

def event_11():
    pass

def event_12():
    pass

def event_13():
    pass

def event_14():
    pass

def event_15():
    master.stop()

pp = Print(count, 1)
trig_score = Score(count)

s.gui(locals())