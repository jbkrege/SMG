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


        start = np.random.randint(x, (x+(window_size - grain_size)))
        stop = start + grain_size
        grain = music[start:stop] * window(grain_size)

        if x is begin:
            output = np.append(output, grain )
        else:
            if overlap is 0:
                postpad = int(grain_size*((2.0 - 0.01) * np.random.random()))
            else:
                postpad = int(grain_size * (overlap))
            output = np.lib.pad(output, (0,postpad), 'constant', constant_values=(0, 0))
            prepad = output.size - grain_size
            grain = np.lib.pad(grain, (prepad,0), 'constant', constant_values=(0, 0))

            output = output + grain

        x += grain_size
         
    return output

def index_feature_vectors(num_feat_vecs, num_samples):
    '''
    INPUT:
        num_feat_vecs: the number of feature vectors computed from the features of a signal
        num_samples: the number of total samples in the signal

    OUTPUT:
        index: a mapping of where each feature vector starts in the terms of indices into the original signal
    '''
    #samps_per_feat = num_samples / num_feat_vecs

    index = np.linspace(0, num_samples, num=num_feat_vecs, dtype=int)

    for x in xrange(len(index)):
        index[x] = int(index[x])

    return index

def granulate_selfsim(music, sim_mat, sr, grain_frac, grains_per_window, overlap, output_size, window_type = 'no window'):
    '''
    INPUT:
        music: the input signal
        sim_mat: a self similarity matrix of the music signal
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

    #similarity matrix setup#
    feat_vec_index = index_feature_vectors(sim_mat[-1].size, music.size)
    #potentially create a new order every iteration
    order = np.random.randint(sim_mat[-1].size, size=sim_mat[-1].size)
    #eventually these will be user defined
    branch = 0.5
    thresh = 0.7
    #END#
    

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


        start = np.random.randint(x, (x+(window_size - grain_size)))
        stop = start + grain_size
        grain = music[start:stop] * window(grain_size)

        if x is begin:
            output = np.append(output, grain )
        else:
            if overlap is 0:
                postpad = int(grain_size*((2.0 - 0.01) * np.random.random()))
            else:
                postpad = int(grain_size * (overlap))
            output = np.lib.pad(output, (0,postpad), 'constant', constant_values=(0, 0))
            prepad = output.size - grain_size
            grain = np.lib.pad(grain, (prepad,0), 'constant', constant_values=(0, 0))

            output = output + grain

        if np.random.random() > branch:
            vec = np.searchsorted(feat_vec_index, x) - 1
            for index in order:
                if sim_mat[vec][index] > thresh and index is not vec:
                    if feat_vec_index[index] < (music.size - window_size):
                        x = feat_vec_index[index]
                        break

        x += grain_size
         
    return output



if __name__ == "__main__":

    print "This is a demo of the granulate function. \nIt generates a 30s output file named grantest.wav. \nIt uses 2ms grains, a selection range of 1000 grains, and a Tukey window."
    path = raw_input("Please enter your .wav file name/path: ")

    music, sr = librosa.load(path)

    test = granulate(music, sr, 0.02, 1000, 0.5, 30, 'tukey')

    librosa.output.write_wav('grantest.wav', test, sr)
