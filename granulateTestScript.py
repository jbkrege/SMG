#!/usr/bin/env

from granulate import *

music, sr = librosa.load('/path/to/your/sound.wav')

#run with set grain size of 20 ms
test = granulate(music, sr, 0.02, 80, 1, 20, 'tukey')

librosa.output.write_wav('grantest.wav', test, sr)

#run with random grain sizes between 10 and 100 ms 
test = granulate(music, sr, 0, 80, 1, 20, 'tukey')

librosa.output.write_wav('grantest2.wav', test, sr)
