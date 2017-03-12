import IPython, numpy as np, matplotlib.pyplot as plt, matplotlib, sklearn, librosa, cmath,math, scipy, time

def one(n):
    return 1

def granulate(music, sr, grain_frac, grains_per_window, overlap, output_size, window_type = 'no window'):
    '''
    INPUT:
        music: the input signal
        sr: the sample rate for the input signal music
        grain_frac: a float representing the grain duration as a fraction of a second. Set to 0 for random grain sizes
            EX: grain_frac = 0.01, grain length is 10 ms
        grains_per_window: how big the range of grains is for the algorithm to pick the next 
            random grain from. Small GpW means not a lot of variety
        overlap: how much will each grain overlap the preceding grain. If 1, grains are 
            added back to back, if < 1, grains over lap, if > 1, space added between grains
        output_size: the duration in seconds of the desired output
        window_type: what type of window will be applied to each grain. 
            Options are Hann and Triangle as of now

    OUTPUT:
        output: A signal of duration output_size that starts from a random position in the song, 
            and proceeds linearly through the song randomly selecting grains from the window and 
            adding them together with the desired overlap.
    '''
    output = np.array([0])
    output_len = output_size * sr

    if grain_frac > 0:
        grain_size = int(sr * grain_frac)
        window_size = grain_size * grains_per_window
    else:
        grain_size = int(sr * 0.05)
        window_size = grain_size * grains_per_window

    if window_type is 'no window':
        window = one
    elif window_type is 'hann':
        window = scipy.signal.hann
    elif window_type is 'triangle':
        window = scipy.signal.triang
    elif window_type is 'tukey':
        window = scipy.signal.tukey
    
    #x = 0
    x = np.random.randint(0, music.size/2)
    begin = x 

    end = begin + output_len
    
    while output.size < output_len:
        if grain_frac is 0:
            grain_size = int(sr*((0.1 - 0.01) * np.random.random())) #+ 0.01
        print grain_size
        start = np.random.randint(x, (x+(window_size - grain_size)))
        stop = start + grain_size
        grain = music[start:stop] * window(grain_size)

        if x is begin:
            output = np.append(output, grain )
        else:
            postpad = int(grain_size * (overlap))
            output = np.lib.pad(output, (0,postpad), 'constant', constant_values=(0, 0))
            prepad = output.size - grain_size
            grain = np.lib.pad(grain, (prepad,0), 'constant', constant_values=(0, 0))

            output = output + grain

        x += grain_size
         
    return output



if __name__ == "__main__":

    print "This is a demo of the granulate function. \nIt generates a 30s output file named grantest.wav. \nIt uses 2ms grains, a selection range of 1000 grains, and a Tukey window."
    music, sr = librosa.load('misuse.wav')

    test = granulate(music, sr, 0.02, 1000, 0.5, 30, 'tukey')

    librosa.output.write_wav('grantest.wav', test, sr)
