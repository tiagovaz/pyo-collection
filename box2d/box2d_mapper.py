from pyo import *
import mapper

s = Server(audio="jack", sr=44100, buffersize=512)
s.boot()

a = BrownNoise()
b1 = Biquadx(a, freq=200, q=10, type=2).out()
b2 = Biquadx(a, freq=400, q=10, type=2).out()
b3 = Biquadx(a, freq=600, q=10, type=2).out()
b4 = Biquadx(a, freq=800, q=10, type=2).out()
b5 = Biquadx(a, freq=1000, q=10, type=2).out()

dev1 = mapper.device("Biquad")
dev2 = mapper.device("Biquad")
dev3 = mapper.device("Biquad")
dev4 = mapper.device("Biquad")
dev5 = mapper.device("Biquad")

dev1_input = dev1.add_input( "/Q", 1, "i", None, 1, 500, lambda s, i, f, t: b1.setQ(f) )
dev1_input = dev1.add_input( "/freq", 1, "i", None, 20, 200, lambda s, i, f, t: b1.setFreq(f) )

dev2_input = dev2.add_input( "/Q", 1, "i", None, 1, 500, lambda s, i, f, t: b2.setQ(f) )
dev2_input = dev2.add_input( "/freq", 1, "i", None, 200, 500, lambda s, i, f, t: b2.setFreq(f) )

dev3_input = dev3.add_input( "/Q", 1, "i", None, 1, 500, lambda s, i, f, t: b3.setQ(f) )
dev3_input = dev3.add_input( "/freq", 1, "i", None, 500, 1000, lambda s, i, f, t: b3.setFreq(f) )

dev4_input = dev4.add_input( "/Q", 1, "i", None, 1, 500, lambda s, i, f, t: b4.setQ(f) )
dev4_input = dev4.add_input( "/freq", 1, "i", None, 1000, 5000, lambda s, i, f, t: b4.setFreq(f) )

dev5_input = dev5.add_input( "/Q", 1, "i", None, 1, 500, lambda s, i, f, t: b5.setQ(f) )
dev5_input = dev5.add_input( "/freq", 1, "i", None, 5000, 12000, lambda s, i, f, t: b5.setFreq(f) )


# detuned waveguides example
src = SfPlayer("/usr/share/doc/python-pyo/examples/snds/ounkmaster.aif", loop=True, mul=.1)

lf = Sine(freq=[random.uniform(.005, .015) for i in range(8)],
          mul=[.02,.04,.06,.08,.1,.12,.14,.16],
          add=[50,100,150,200,250,300,350,400])
lf2 = Sine(.005, mul=.2, add=.7)

det_wg = AllpassWG(src, freq=lf, feed=.999, detune=lf2, mul=.25)

dev6 = mapper.device("WG")
dev6_input = dev6.add_input( "/feedback", 1, "f", None, 0.1, 1, lambda s, i, f, t: det_wg.setFeed(f) )
dev6_input = dev6.add_input( "/detune", 1, "f", None, 0.5, 0.9, lambda s, i, f, t: det_wg.setDetune(f) )

s.start()

while 1:
    dev1.poll(10)
    dev2.poll(10)
    dev3.poll(10)
    dev4.poll(10)
    dev5.poll(10)
    #dev6.poll(10)