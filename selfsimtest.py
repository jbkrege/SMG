#!/usr/bin/env

from simmatrix import *
from granulate import *

print "Load music"
music, sr = librosa.load('twinpeaks.wav', sr=500, duration=30)

print "Compute chroma features"
chroma = librosa.feature.chroma_stft(music, sr)

print "Compute Self Similarity Matrix"
selfsim = sim_matrix(chroma, sr, 0, distance_metric = 'cosine', display = False)

print "Run SelfSim Granulator"
test = granulate_selfsim(music, selfsim, sr, 0, 100, 1, 30, 'tukey')

print "write output to wav"
librosa.output.write_wav('grantest.wav', test, sr)

