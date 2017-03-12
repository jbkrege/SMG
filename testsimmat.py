#!/usr/bin/env

from simmatrix import *

music, sr = librosa.load('misuse.wav')

music2, sr2 = librosa.load('call_me_maybe.wav')

chroma = librosa.feature.chroma_stft(music, sr)
chroma2 = librosa.feature.chroma_stft(music2, sr2)

print "Chroma shape: ", chroma.shape
print "Chroma2 shape: ", chroma2.shape

crosssim = cross_sim_matrix(chroma, chroma2, sr, 0, distance_metric = 'cosine')

#test = sim_matrix(chroma, sr, 0, distance_metric = 'cosine', display = False)

print crosssim.shape

#cepstra = librosa.feature.mfcc(music, sr)

#print "Cepstra shape: ", cepstra.shape
