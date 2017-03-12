#!/usr/bin/env

from granulate import *

music, sr = librosa.load('misuse.wav')

test = granulate(music, sr, 0.02, 80, 1, 20, 'tukey')

librosa.output.write_wav('grantest.wav', test, sr)

test = granulate(music, sr, 0, 80, 1, 20, 'tukey')

librosa.output.write_wav('grantest2.wav', test, sr)
