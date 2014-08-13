# Introduction to Pyo: a Python module for digital signal processing

---

# About

## Pyo
- Written in C, focused on performance (and simplicity!)
- Free software, under GNU/GPL license
- Great API documentation (created using Sphinx)
- Supports OSC and MIDI
- Multi-plataform (though it's easier to get it running in Linux)
- Credits to [Olivier Bélanger](http://musique.umontreal.ca/personnel/belanger_o.html), creator and main developer of Pyo
- Project details at [http://ajaxsoundstudio.com/software/pyo/](http://ajaxsoundstudio.com/software/pyo/)

## Me
- Music student, curious about computers
- Maintainer of RadioPyo and Pyo packages for Debian/Ubuntu
- Wrote this presentation, available under CC BY 4.0

---

# Getting started

## Simple sine output

    !python
    from pyo import *
    s = Server()                # create a pyo server object
    s.boot()                    # boot the server
    sin = Sine(mul=0.5)         # start a single sine stream
    sin.out()                   # send this sine stream to audio ouput
    s.start()                   # start the server

## Pyo server
    !python
    Server(sr=44100, nchnls=2, buffersize=256, duplex=1, audio='portaudio')

---

# Basic features

## Interaction with Pyo server
    !python
    s.gui(locals())

## Setting object values
    !python
    a = Sine(freq=1000, phase=0, mul=1, add=0)
    a = Sine(440, 0, 0.1)
    a.setFreq(440)
    a.freq = 440
    # PyoObject to replace any attribute with portamento:
    a.set(attr="freq", value=600, port=5)

## Setting many audio streams at once
    !python
    a = Sine(freq=[ x*40 for x in range(7) ], mul=[.2, .08, .07, .02, .08, .1, .09])

## Chaining objects
    !python
    freq = Sine(freq=1, mul=30)
    sin = Sine(freq=freq + 440, mul=.5).out()
---

# Important methods

- play()
- out()
- stop()
- ctrl()
- graph()
---

# Pyo classes categories

- Audio Signal Analysis
- Arithmetic
- Control Signals
- Dynamic management
- Special Effects
- Filters
- Fast Fourier Transform
- Phase Vocoder
- Signal Generators
- Internal objects
- Matrix Processing
- Midi Handling
- Open Sound Control
- Routing
- Event Sequencing
- Soundfile Players
- Random generators
- Table Processing
- Sample Accurate Timing (Triggers)
- Tables
- ...

# Examples
## Getting a (sort of) chorus effect from an audio file

    !python
    from pyo import *
    s = Server(audio='jack').boot()
    a = SfPlayer(path="/usr/share/doc/python-pyo/examples/snds/baseballmajeur_m.aif",
                 speed=[1,1.005,1.007,.992], loop=True, mul=.25).out()
    s.gui(locals())

## Exploring some harmonicity with FM

    !python
    from pyo import *
    import random
    s = Server().boot()
    car = [random.triangular(150, 155) for i in range(10)]
    rat = [random.choice([.25, .5, 1, 1.25, 1.5, 2]) for i in range(10)]
    ind = [random.randint(2, 6) for i in range(10)]
    fm = FM(carrier=car, ratio=rat, index=ind, mul=.05).out()
    s.gui(locals())

---

# Examples
## Filtering noise to build a (convincing) wind
    !python
    from pyo import *
    import random
    s = Server().boot()
    
    noise = BrownNoise(mul=Randi(0.5,1))
    j = Randi(1,1.4,Randi(.5,1))

    freqs1 = Randi(150, 300)
    q1 = Randi(4, 6)
    f1 = ButBP(noise, freq=freqs1, q=q1, mul=.2*j)

    freqs2 = [Randi(300, 400)*j for i in range(3)]
    q2 = Randi(40, 300)
    f2 = ButBP(noise, freq=freqs2, q=q2, mul=j*1.5)

    freqs3 = [Randi(2990, 3000)*j for i in range(2)]
    q3 = Randi(10, 33)
    f3 = ButBP(noise, freq=freqs3, q=q3, mul=.01)

    freqs4 = [Randi(10000, 10100)*j for i in range(2)]
    q4 = Randi(10, 33)
    f4 = ButBP(noise, freq=freqs4, q=q4, mul=.01)

    fad = Fader(fadein=1).play()
    m = Mix([f1, f2, f3, f4],voices=2, mul=fad).out()
    s.gui(locals())
---

# Examples
## Now let's write our first 4 voices composition!

    !python
    from pyo import *
    
    s = Server().boot()
    
    pitches = [midiToHz(m) for m in [36,43,48,55,60,62,64,65,67,69,71,72]]
    
    # Add more voices here to generate a simple counterpoint
    choice = Choice(choice=pitches, freq=1)
    ch_port = Port(choice, risetime=.001, falltime=.001)
    
    # Two simple instruments
    lfdetune = Sine(freq=0.1, mul=.07, add=.07)
    instrument1 = SuperSaw(freq=ch_port, detune=lfdetune, mul=.1)
    lfind = Sine(freq=0.1, phase=0.5, mul=3, add=3)
    instrument2 = FM(carrier=ch_port, ratio=1.0025, index=lfind, mul=.025)
    
    # Send instruments output to delay
    src_sum = instrument1.mix(2) + instrument2.mix(2)
    lfdel = Sine(.1, mul=.003, add=.005)
    comb = Delay(src_sum, delay=lfdel, feedback=.5)
    
    # Send two resulting signals to reverb and output
    out_sum = src_sum + comb
    rev = STRev(out_sum, cutoff=3500, bal=.5, roomSize=2).out()
    
    s.gui(locals())
---

# Event sequencing
## Pyo offers different directions for event sequencing
- class Score(input, fname='event_')
- class Pattern(function, time=1)
- class TrigFunc(input, function, arg=None)

---

# Score

    !python
    from pyo import *
    s = Server().boot()
    
    def event_0():
        print "Introduction"
    
    def event_1():
        pass
    
    def event_2():
        print "Profit"
    
    met = Metro(time=1).play()
    count = Counter(met, min=0, max=3)
    score = Score(count, fname="event_")

    s.gui(locals()

---

# TrigFunc

    !python
    from pyo import *
    s = Server().boot()

    time = -1

    def score():
        global time
        time += 1
    
        if time == 1:
            print "Introduction"
    
        if time == 15:
            print "Profit!"
    
    mainTime = Metro(time=1).play()
    mainFunc = TrigFunc(mainTime, score)
    s.gui(locals())

---
# Pattern

    !python
    from pyo import *

    s = Server().boot()

    t = HarmTable([1,0,.33,0,.2,0,.143,0,.111])
    a = Osc(table=t, freq=[250,251], mul=.2).out()

    def pat():
        f = random.randrange(200, 401, 25)
        a.freq = [f, f+1]

    p = Pattern(pat, .125)
    p.play()
    s.gui(locals())

---

# Triggers

A trigger in Pyo is an audio signal with a value of 1 surrounded by 0s.

## Examples of trigger 'generators':
- **Metro**: Generates isochronous trigger signals.
- **Beat**: Generates algorithmic trigger patterns.
- **Thresh**: Sends a trigger when a signal crosses a threshold.
- **Cloud**: Generates random triggers with control over the generation density.

## Examples of trigger 'receivers':

- **TrigEnv**: Starts reading an envelope in x seconds each time it receives a trigger.
- **TrigFunc**: Calls a given function each time it receives a trigger.
- **TrigXnoise**: A new value is generated each time the object receive a trigger in input. Some of available distributions are uniform, linear min/max, triangular, exp min/max, gaussian, loopseg...
- **TrigXnoiseMidi**: Same as above, but generates MIDI notes instead. It receives a MIDI range as parameter.

---

# Examples
## Playing with triggers and performing our first canon :)
    !python
    from pyo import *
    s = Server(audio='jack').boot()
    
    # Builds an amplitude envelope in a linear table
    env = LinTable([(0,0), (190,.8), (1000,.5), (4300,.1), (8191,0)], size=8192)
    env.graph()
    
    # Metronome provided by Beat
    met = Beat(time=.125, taps=16, w1=90, w2=50, w3=30).play()
    
    # Reads the amp envelope for each trigger from Beat
    amp = TrigEnv(met, table=env, dur=met['dur'], mul=met['amp'])
    
    # Generates a midi note for each trigger from Beat in a pseudo-random distribution
    fr = TrigXnoiseMidi(met, dist=12, x1=1, x2=.3, scale=0, mrange=(48,85))
    
    # Receives the midi note from XnoiseMidi and scale it into C harmonic minor (try others!)
    frsnap = Snap(fr, choice=[0,2,3,5,7,8,11], scale=1)
    
    # This instrument receives a frequency from Snap and molde it inside an envelop from TrigEnv
    lfo = Sine(freq=.05, mul=.05, add=.08)
    gen = SineLoop(freq=frsnap, feedback=lfo, mul=amp*.5).out(0)
    
    # Output the same signal with some delay in the right speaker (try a 'real' counterpoint!)
    rev = Delay(gen, delay=[.25, .5], feedback=.3, mul=.8).out(1)

    s.gui(locals())

---

# Examples
## MIDI out

    !python
    from pyo import *
    from random import *
    
    s = Server(audio='jack')
    s.setMidiOutputDevice(3)
    s.boot()
    
    def playsoprano():
        s.sendMidiNote(choice([60, 62, 63, 65, 67, 68, 71]), randint(30,100), channel=1)
    
    def playtenor():
        s.sendMidiNote(choice([48, 50, 51, 53, 55, 56, 59]), randint(50,60), channel=2)
    
    def playbass():
        s.sendMidiNote(choice([36, 36, 36, 41, 48]), randint(80,100), channel=3)
    
    met = Beat(time=.5, taps=16, w1=80, w2=60, w3=40).play()
    p = TrigFunc(met, playsoprano).play()
    
    met2 = Beat(time=1, taps=16, w1=70, w2=50, w3=30).play()
    p2 = TrigFunc(met2, playtenor).play()
    
    met3 = Beat(time=1, taps=16, w1=100, w2=20, w3=10).play()
    p3 = TrigFunc(met3, playbass).play()
    
    s.gui(locals())


---

# Examples
## Open Sound Control - server
    !python
    from pyo import *
    s = Server().boot()
    lfo = Sine(.05, mul=.5, add=.5)
    rnd = Sig(0)
    rnd.ctrl()
    send = OscSend([lfo, rnd], port=9000, address=['/pos','/rand'], host='127.0.0.1')
    s.gui(locals())

## Open Sound Control - client
    !python
    from pyo import *
    s = Server(audio="jack").boot()
    table = SndTable("transparent.aif")
    env = HannTable()
    rec = OscReceive(port=9000, address=['/pos', '/rand'])
    pos = Port(rec['/pos'], risetime=.05, falltime=.05, mul=table.getDur()*44100.)
    pit = [1., 1.002]
    dur = Noise(mul=Clip(rec['/rand'], min=0, max=.09), add=.1)
    grain = Granulator( table=table,    
                        env=env,       
                        pitch=pit,    
                        pos=pos,     
                        dur=dur,    
                        grains=32, 
                        basedur=.1,
                        mul=.1).out()
    s.gui(locals())


---


# Pyo Ecosystem

## Software
- [Cecilia5](http://ajaxsoundstudio.com/software/cecilia/): audio signal processing environment
- [Zyne](http://code.google.com/p/zyne): modular soft synthesizer
- [Soundgrain](http://code.google.com/p/soundgrain): graphical interface where users can draw and edit trajectories to control granular sound synthesis
- [RadioPyo](http://radiopyo.acaia.ca): live python music (compositions code [available](https://github.com/tiagovaz/radiopyo))
- [PsychoPy](http://www.psychopy.org): application to allow the presentation of stimuli and collection of data for a wide range of neuroscience, psychology and psychophysics experiments.

## Discussion
- [https://groups.google.com/forum/#!forum/pyo-discuss](https://groups.google.com/forum/#!forum/pyo-discuss)

---

# Thanks!
