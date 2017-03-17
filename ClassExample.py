from Granulator import *

#g = Granulator('../sounds/reich.wav','../sounds/phaedra.wav')
g = Granulator('../sounds/reich.wav','../sounds/reich.wav')

g.setFeatures(0)
g.Print()
g.run("../output/reich_chroma.wav")

g.setFeatures(1)
g.Print()
g.run("../output/reich_mfcc.wav")