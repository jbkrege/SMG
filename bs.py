from pyo import*
import time

# Play soundfile


def playSound(src):
	s = Server().boot()
	s.start()
	sf = SfPlayer(src,speed=1,
	 loop=True).out()

# playSound("/Users/Ben/Desktop/MT340/proj3/lux.aif")

def granulate():
	s = Server().boot()
	# a = FM(carrier = 150, ratio = .4958, index = 10, mul = .2)
	# a.ctrl(title = "Frequency modulation controls")
	# b = a.mix(2)
	# b.out()
	s.start()
	snd = SndTable("/Users/Ben/Desktop/MT340/proj3/lux.aif")
	env = HannTable()
	pos = Phasor(freq=snd.getRate()*.25, mul=snd.getSize())
	dur = Noise(mul=.001, add=.1)
	g = Granulator(snd, env, [1, 1.001], pos, dur, 32, mul=.1).out()
	g.ctrl(title = "Granulation Controls")
	# b = g.mix()
	# b.out(2)
	# Second voice
	# snd2 = SndTable("/Users/Ben/Desktop/MT340/proj3/crowd1.aif")
	# g2 = Granulator(snd2, env, [1, 1.001], pos, dur, 32, mul=.1).out()
	s.gui(locals())

granulate()