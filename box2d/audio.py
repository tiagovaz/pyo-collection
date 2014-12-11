from pyo import *

class Bass():
    def __init__(self):
        self.mul = .3
        self.freq = [random.uniform(100, 400) for i in range(2)]
        self.t = LinTable([(0, 0.0000), (35, 0.9896), (4290, 0.6528), (5932, 0.2280), (7732, 0.1503), (8191, 0.0000)])
        self.amp = TableRead(self.t, freq=.5, loop=False).stop()
        self.sin = SineLoop(freq=self.freq, feedback=.05, mul=self.amp).stop()
        self.delay = Delay(self.sin, delay=[0.01, 0.038, 0.72], feedback=0, mul=[1, .78, .29]).stop()
        self.fade = Fader(fadein=.1, fadeout=50).stop()
        self.outsig = Mix(self.delay, voices=2, mul=self.mul * self.fade).stop()
        self.play()

    def setfreq(self, freq):
        self.sin.freq = freq

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

class BG:
    def __init__(self):
        self.mul = .3
        self.freq = [random.uniform(40, 1200) for i in range(2)]
        self.sin = Sine(freq=self.freq, mul=.01).stop()
        self.fade = Fader(fadein=.1, fadeout=5).stop()
        self.outsig = Mix(self.sin, voices=2, mul=self.mul * self.fade).stop()
        self.play()

    def setfreq(self, freq):
        #print '%f seconds since last callback' % float(dt*10000)
        self.sin.setFreq(freq)

    def stop(self):
        self.outsig.stop()

    def play(self):
        self.sin.play()
        self.fade.play()
        self.outsig.out()

    def tail(self):
        self.fade.stop()