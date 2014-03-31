#!/usr/bin/env python
# encoding: utf-8

from pyo import *
import random

# Simple wind generator with Pyo
# Tiago Bortoletto Vaz <tiago@debian.org>
# Public domain - Wed Oct  9 15:27:32 EDT 2013

s = Server().boot()

# Brown noise to have less high frequency to cutoff
noise = BrownNoise(mul=Randi(0.5,1))

# This gives a factor for both the wind intensity and frequency. Intensity
# and frequency go together in the two first filters in order to generate a
# more natural wind. Q variation gives a kind of wind blows.
j = Randi(1,1.4,Randi(.5,1))

# Filter 1 - sort of continuos bass wind
freqs1 = Randi(150, 300)
q1 = Randi(4, 6)
f1 = ButBP(noise, freq=freqs1, q=q1, mul=.2*j)

# Filter 2 - main wind frequency with slow variation, following wind intensity
freqs2 = [Randi(300, 400)*j for i in range(3)]
q2 = Randi(40, 300)
f2 = ButBP(noise, freq=freqs2, q=q2, mul=j*1.5)

# Filter 3 - very high component, almost fixed in frequency
freqs3 = [Randi(2990, 3000)*j for i in range(2)]
q3 = Randi(10, 33)
f3 = ButBP(noise, freq=freqs3, q=q3, mul=.01)

# Filter 4 - the highest frequency wind component, also quite fixed
freqs4 = [Randi(10000, 10100)*j for i in range(2)]
q4 = Randi(10, 33)
f4 = ButBP(noise, freq=freqs4, q=q4, mul=.01)

# Player
fad = Fader(fadein=1).play()
m = Mix([f1, f2, f3, f4],voices=2, mul=fad).out()

s.gui(locals())
