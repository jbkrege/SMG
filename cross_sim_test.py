#!/usr/bin/env

from simmatrix import *
from granulate import *

print "Load Music"
song1, sr1 = librosa.load('forestsounds.wav')
song2, sr2 = librosa.load('lux.wav')

print "Compute Cepstral features"
size = song1.size
#lux_cepstra = librosa.feature.mfcc(lux[(size/4):(3*size/4)], sr1)
#lux_chroma = librosa.feature.chroma_stft(lux[(size/4):(3*size/4)], sr1)
#song1_chroma = librosa.feature.chroma_stft(song1, sr1)
song1_cepstra = librosa.feature.mfcc(song1, sr1)

#size = forest.size
#forest_cepstra = librosa.feature.mfcc(forest, sr2)
#song2_chroma = librosa.feature.chroma_stft(song2, sr2)
song2_cepstra = librosa.feature.mfcc(song2, sr2)

print "Compute Cross Similarity Matrix"
crosssim = cross_sim_matrix(song1_cepstra, song2_cepstra, sr1, 0, distance_metric = 'cosine', display = False)

print "Run SelfSim Granulator"
test = granulate_crosssim(song1, song2, crosssim, sr1, 0, 200, 0, 30, 'hann')

print "write output to wav"
librosa.output.write_wav('crosstest.wav', test, sr1)
