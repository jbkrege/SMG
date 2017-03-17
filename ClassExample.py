from Granulator import *

g = Granulator('../sounds/birds.wav','../sounds/fireplace.wav')
g.Print()
g.run("../sounds/birds_fireplace.wav")

g.setGrainlen(0.5)
g.Print()
g.run("../output/birds_fireplace_long_grain.wav")

g.setGrainlen(0.02)
g.Print()
g.run("../output/birds_fireplace_short_grain.wav")