from Granulator import *

g = Granulator('birds.wav','fireplace.wav')
g.Print()
g.run("../sounds/birds_fireplace.wav")

g.setGrainLen(0.5)
g.Print()
g.run("../sounds/birds_fireplace_long_grain.wav")

g.setGrainLen(0.02)
g.Print()
g.run("../sounds/birds_fireplace_short_grain.wav")