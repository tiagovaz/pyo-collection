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
from music21 import *
from Markov import Markov
from random import *

# for markov
midi_velocity = randint(10, 100)

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


class Bass():
    def __init__(self, mul=.3, freq=[24, 24.5]):
        self.t = LinTable([(0, 0.0000), (35, 0.9896), (4290, 0.6528), (5932, 0.2280), (7732, 0.1503), (8191, 0.0000)])
        self.t.graph()
        self.amp = TableRead(self.t, freq=.5, loop=False).stop()
        self.sin = SineLoop(freq=freq, feedback=.05, mul=self.amp).stop()
        self.delay = Delay(self.sin, delay=[0.01, 0.038, 0.72], feedback=0, mul=[1, .78, .29]).stop()
        self.fade = Fader(fadein=.01, fadeout=.01).stop()
        self.outsig = Mix(self.delay, voices=2, mul=mul * self.fade).stop()

    def play(self):
        self.amp.play()
        self.sin.play()
        self.delay.play()
        self.fade.play()
        self.outsig.out()

    def tail(self):
        self.fade.stop()

    def stop(self):
        self.amp.stop()
        self.sin.stop()
        self.delay.stop()
        self.outsig.stop()


class Background():
    def __init__(self, freq=1000, q=2, mul=1):
        self.gamp = Expseg([(0, 0), (20, 1), (20.05, 0)], exp=4, mul=mul)  # global amp
        self.lff = Lorenz(0.1, 0.7).range(200, 5000).stop()  # freq control
        self.lfc = Lorenz(0.05, 0.7).range(0.2, 0.5).stop()  # feedback control
        self.gen = SineLoop(freq=self.lff, feedback=self.lfc, mul=0.01).stop()
        self.fade = Fader(fadein=.1, fadeout=.1).stop()
        self.bpfilter = ButBP(self.gen, freq=freq, q=q, mul=self.gamp).stop()
        self.outsig = Mix(self.bpfilter, mul=self.fade * mul).stop()

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


class Rumble():
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


class RhythmFou():
    def __init__(self, pitch=1177.6, beat_freq=4, fadein=100, fadeout=.01, mul=1):
        self.t = LinTable(
            [(0, 0.0000), (0, 0.8187), (1271, 0.7358), (1412, 0.6788), (2489, 0.5907), (3584, 0.4093), (4731, 0.2124),
             (4802, 0.0881), (4802, 0.1140), (5526, 0.1036), (6179, 0.0829), (6532, 0.0622), (6673, 0.0000),
             (7150, 0.0000), (8191, 0.0000)])
        self.amp = TableRead(table=self.t, freq=beat_freq, loop=True, mul=.3 * mul).stop()
        self.sin = SineLoop(freq=[45.8, pitch], feedback=.0885, mul=self.amp).stop()
        self.delay = Delay(self.sin, delay=[0.00371, 0.00190, 0.00131], feedback=0.1692, mul=[1.8, 0.4, 0.086]).stop()
        self.gamp = Fader(fadein=fadein, fadeout=fadeout).stop()
        self.outsig = Mix(self.delay, voices=2, mul=self.gamp).stop()

    def play(self):
        self.amp.play()
        self.gamp.play()
        self.sin.play()
        self.delay.play()
        self.outsig.out()

    def tail(self):
        self.gamp.stop()

    def stop(self):
        self.sin.stop()
        self.amp.stop()
        self.delay.stop()
        self.outsig.stop()


class Rhythm():
    def __init__(self, freq=2, mul=1):
        self.lf = Sine(uniform(.02, .05)).range(.3, .8).stop()
        self.v1 = SineLoop(freq=freq, feedback=self.lf, mul=0.02).stop()
        self.v2 = SineLoop(freq=freq, feedback=self.lf * 0.95, mul=0.02).stop()
        self.fade = Fader(fadein=0.01, fadeout=0.01)
        self.outsig = Mix([self.v1, self.v2], voices=2, mul=mul * self.fade).stop()

    def play(self):
        self.lf.play()
        self.v1.play()
        self.v2.play()
        self.outsig.out()

    def tail(self):
        self.fade.stop()

    def stop(self):
        self.lf.stop()
        self.v1.stop()
        self.v2.stop()
        self.outsig.stop()

class MyDelay:
    """A sensor controls delay/reverb of an audio stream
       - audio1 being an Input() signal
       - audio2 being a sensor output (audio stream) from 0 to 1
       - audio3 being a sensor output (audio stream) from 40 to 800
    """
    #TODO: no mess, take fadein/out as argument
    def __init__(self, audio1, audio2=.01, audio3=40, mul=.7):
        self.lfd = Sine([.4,.3], mul=.2, add=.5)
        self.supersaw = SuperSaw(freq=[ audio3*uniform(0.94, 1.04) for i in range(10) ], detune=self.lfd, bal=0.7, mul=.1)
        self.r = Freeverb(self.supersaw, size=.94, damp=.87, bal=.9, mul=1)
        self.d2 = Delay(self.r, delay=audio2, feedback=uniform(0.95, 1), mul=.4)
        self.d3 = Delay(self.d2, delay=[.05, .1, .25, .5], feedback=.25, mul=.4)
        #self.c = Chorus(audio1, depth=[1.5,1.6], feedback=0.5, bal=0.5)
        self.r2 = Freeverb(audio1, size=.74, damp=.87, bal=.5, mul=1)
        self.d4 = Delay(self.r2, delay=audio2, feedback=uniform(0.95, 1), mul=.6)
        #self.mix = Freeverb(Mix(self.d2 + self.d3 + self.r2 + self.d4, mul=.7), size=.34, damp=.37, bal=.9, mul=.9)
        self.amp = Fader(fadein=20, fadeout=20)
        self.mix = Mix(self.d2 + self.d3 + self.r2 + self.d4, mul=self.amp*mul).out()

    def play(self):
        self.amp.play()
        return self

    def stop(self):
        self.amp.stop()
        return self

    def getOut(self):
        return self.amp

    def setInput(self, x, fadetime=.001):
        self.input.setInput(x, fadetime)

class HighFreq():
    def __init__(self, freq=[11200, 11202], dur=.4, mul=.5):
        self.amp = Fader(fadein=.01, fadeout=.01, dur=dur, mul=mul)
        self.sine = SineLoop(freq=freq, mul=self.amp * .05).out()
        self.rev = Freeverb(self.sine, size=.84, damp=.87, bal=.9, mul=self.amp * .2).out()

    def setDur(self, dur):
        self.amp.dur = dur
        return self

    def play(self):
        self.amp.play()
        return self

    def stop(self):
        self.amp.stop()
        return self

    def getOut(self):
        return self.amp


class SmoothNoise():
    def __init__(self, dur=1.3, mul=.5):
        self.amp = Fader(fadein=.1, fadeout=.01, dur=dur, mul=mul)
        self.noise = PinkNoise(self.amp * .01).mix(2).out()

    def setDur(self, dur):
        self.amp.dur = dur
        return self

    def play(self):
        self.amp.play()
        return self

    def stop(self):
        self.amp.stop()
        return self

    def getOut(self):
        return self.amp

    def setInput(self, x, fadetime=.001):
        self.input.setInput(x, fadetime)


class DarkBackground():
    def __init__(self, fadein=100, p1=.2054, p2=[.3966, .3933], chaos1=.4038, chaos2=.0769, feedback=.5, mul=.5):
        self.r1 = Rossler(pitch=p1, chaos=chaos1, stereo=True, mul=.5, add=.2).stop()
        self.r2 = Rossler(pitch=p2, chaos=chaos2, mul=self.r1 * .2).stop()
        self.amp = Fader(fadein=fadein, fadeout=5).stop()
        self.outsig = Delay(self.r2, feedback=feedback, mul=self.amp * mul).stop()

    def play(self):
        self.r1.play()
        self.r2.play()
        self.amp.play()
        self.outsig.out()

    def tail(self):
        self.amp.stop()

    def stop(self):
        self.r1.stop()
        self.r2.stop()
        self.outsig.stop()

class MyGranulator:
    #FIXME: finish him!
    def __init__(self, input):
        snd = SndTable(input)
        env = HannTable()
        pos = Phasor(freq=snd.getRate()*.25, mul=snd.getSize())
        dur = Noise(mul=.001, add=.1)
        g = Granulator(snd, env, [1, 1.001], pos, dur, 32, mul=.1).out()

    def play(self):
        pass

    def stop(self):
        pass

class MyRev:
    def __init__(self, input):
        self.rev = STRev(input, inpos=0.25, revtime=2, cutoff=5000, bal=0.25, roomSize=1).stop()
        self.rev.ctrl()

    def play(self):
        self.rev.out()

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
            self.current_beat = 0
        self.current_beat += 1

    def play(self):
        self.p.play()

    def stop(self):
        self.p.stop()

############ START MARKOV PLAYER ######################

class MarkovMidiPlayer:
    """
    - midi_velocity = int 0 to 127
    - midi_duration = int
    - midi_channels = list of int
    - midi_transpo = int
    - melody = list of int (midi notes)
    - markov_order = int
    - markov_time: list of float
    """
    #TODO: aceitar objetos Pyo como parâmetros
    def __init__(self, markov_order=2, melody=None, markov_time=[.125, .25, 1, 5, 10, 20],
                 midi_channels=[1], midi_velocity=[100], midi_duration=[300],
                 midi_transpo=0):

        # Getting some corpus from music21 library and putting them in a dictionary
        # note1: you can use 'elements' attribute to fetch a voice in the part
        # note2: you can see the score anytime using method 'show()'
        self.index = 0
        self.markov_order = markov_order
        self.markov_time = markov_time
        self.midi_channels = midi_channels
        self.midi_velocity = midi_velocity
        self.midi_duration = midi_duration
        self.midi_transpo = midi_transpo

        self.melodies = {
            'bach': corpus.parse("bach/bwv30.6").getElementById('Bass'),
            'schoenberg': corpus.parse("schoenberg/opus19/movement2").getElementById('P1-Staff1'),
            'albeniz': corpus.parse("albeniz/asturias").getElementById("P1-Staff2")
        }

        # Choose one of the corpus above to be the played melody
        al = self.melodies['albeniz']
        sc = self.melodies['schoenberg']
        ba = self.melodies['bach']

        # Getting notes in midi standard
        self.pitches_a = [i.midi for i in al.pitches]
        self.pitches_s = [i.midi for i in sc.pitches]
        self.pitches_b = [i.midi for i in ba.pitches]

        self.pitches = [self.pitches_a, self.pitches_s, self.pitches_b]

        self.current_melody = choice(self.pitches)

        # Initialize the object
        self.marko = Markov(order=self.markov_order)

        # Start the record mode
        self.marko.mkStartRecord()

        # Record a list of pitches in one pass
        self.marko.mkSetList(self.current_melody)

        # Start the playback mode
        self.marko.mkStartPlayback()

        # markov_time = Choice([.125, .25, .5, 5, 10, 20, 30])
        self.pattern = Pattern(function=self.pick_a_note, time=Choice(self.markov_time))

        # dens = Expseg([(0, 0), (80, 100)], exp=10).play()
        # dens.graph()
        # markov_trig = Cloud(density=dens, poly=5).stop()
        # markov_cloud = TrigFunc(markov_trig, pick_a_note).play()

    # Function called by the Pattern object
    def pick_a_note(self):
        # Pick the next note from the Markov generator
        mid = self.marko.next()

        # Use this one!
        s.sendMidiNote(mid+self.midi_transpo, choice(self.midi_velocity),
                       channel=choice(self.midi_channels), timestamp=choice(self.midi_duration))

        # Testing a more linear output
        #s.sendMidiNote(mid, 100, channel=0, timestamp=500)

    def play_melody(self):
        # Use this to hear the original melody
        if self.index < len(pitches) - 1:
            index = self.index + 1
        else:
            iself.ndex = 0
        note = pitches[self.index]
        s.sendMidiNote(note, 100, channel=choice(self.midi_channels), timestamp=300)

    def setMelody(self, melody):
        # go random
        #marko.mkSetList(choice([pitches_s, pitches_b, pitches_a]))
        self.current_melody = melody
        self.marko.mkSetList(self.current_melody)
        self.marko.mkStartPlayback()

    def setMarkovTime(self, time):
        self.markov_time = time

    def setMarkovOrder(self, order):
        self.markov_order = order

    def setMidiChannels(self, channels):
        self.midi_channels = channels

    def setMidiVelocity(self, velocity):
        self.midi_velocity = velocity

    def setMidiDuration(self, duration):
        self.midi_duration = duration

    def setTranspo(self, transpo):
        self.midi_transpo = transpo

    def play(self):
        self.pattern.play()


################ END MARKOV PLAYER ####################

s = Server(audio='jack', sr=44100, nchnls=2, buffersize=512, duplex=1).boot()
s.startoffset = 65
# Set midi device (use pm_list_devices() to list them)
s.setMidiOutputDevice(5)

# Markov
markov_player = MarkovMidiPlayer()

# Sparks
sparks = Sparks(mul=.3)

# Rumble
rumble = Rumble(mul=1)

# Background
back1 = Background(freq=400, q=4, mul=3)
back2 = Background(freq=700, q=4, mul=3)
back3 = Background(freq=2700, q=4, mul=3)

# Rhythm
rhythm1 = Rhythm(freq=.04, mul=.005)
rhythm2 = RhythmFou(mul=.02, fadein=30, fadeout=.01, beat_freq=5)
rhythm3 = RhythmFou(mul=.015, pitch=1200, fadein=1, beat_freq=10)
rhythm4 = RhythmFou(mul=.01, pitch=632, fadein=5, beat_freq=5)
rhythm5 = RhythmFou(mul=.015, pitch=590, fadein=.01, beat_freq=5)

# Bass background
sd1 = Sine([36.71, 36], mul=0.05).out(delay=70, dur=0)
sd2 = Sine([72, 73], mul=0.015).out(delay=70, dur=0)
sd3 = Sine([144, 144.2], mul=0.015).out(delay=90, dur=0)
darkback = DarkBackground(mul=.2)
darkback2 = DarkBackground(p2=[.203, .116], chaos1=.39, mul=.4)

#mydelay = MyDelay(Input(mul=.1), 1, 1000, 1)
instruments_rev = MyRev(Input(mul=.8))

# Random high freqs
# env2 = LinTable([(0, 0.0000), (0, 1.0000), (1694, 1.0000), (1694, 0.0000), (8192, 0.0000)])
# rnddur = RandDur(min=[1, 1, 1, 1], max=4)
# tenv2 = Change(rnddur)
# amp2 = TrigEnv(tenv2, env2, rnddur, mul=0.001)
# fr = TrigRand(tenv2, min=7000, max=12000)
# syns = Sine(freq=fr, mul=amp2 * .5).out(delay=100, dur=0)

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
    # markov_trig.play()

def event_2():
    pass

def event_3():
    pass

def event_4():
    rhythm2.play()

def event_5():
    back1.play()
    back2.play()
    back3.play()

def event_6():
    pass

def event_7():
    markov_player.play()
    instruments_rev.play()
    rhythm1.play()
    rhythm2.tail()
    sparks.tail()
    back1.tail()
    back2.tail()
    back3.tail()
    rumble.tail()
    darkback2.play()

def event_8():
    #markov_player.setMelody([40, 41, 42, 43, 44, 45])
    rhythm2.stop()
    back1.stop()
    back2.stop()
    back3.stop()
    rumble.stop()
    sparks.stop()
    darkback.play()

def event_9():
    p_bass1.play()  # rhythm pattern
    p_bass2.play()  # rhythm pattern
    p_noise.play()  # rhythm pattern


def event_10():
    p_high.play()


def event_11():
    rhythm3.play()


def event_12():
    pass


def event_13():
    rhythm4.play()


def event_14():
    rhythm5.play()


def event_15():
    master.stop()


pp = Print(count, 1)
trig_score = Score(count)

bass = Bass(mul=.4, freq=[24, 24.1, 24.5])
bass2 = Bass(mul=.6, freq=[24, 24.1, 24.5])
snoise = SmoothNoise(mul=.2)
high = HighFreq(mul=.10)

p_bass1 = MyPattern(bass, time=.125, beats=64, beats_to_play=[1])
p_bass2 = MyPattern(bass2, time=.125, beats=64, beats_to_play=[3, 32])
p_noise = MyPattern(snoise, time=.125, beats=64, beats_to_play=[31])
p_high = MyPattern(high, time=.125, beats=64, beats_to_play=[3, 33])

s.gui(locals())
