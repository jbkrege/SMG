import IPython, numpy as np, sklearn, librosa, cmath,math, scipy, time

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
        if start > end or stop > end:
            continue
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
    branch = 0.3
    thresh = 0.4
    breakout = 0.9
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
        #if we reached the end of the track, jump to a new place
        if (x + window_size) >= music.size:
            x = np.random.randint(0, music.size/2)
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
        #break out of the same feature we are stuck in
        if np.random.random() > breakout:
            x = np.random.randint(0, music.size)
        x += grain_size

    return output


#TODO
#1 Cross sim granulate
#2 make parameters more intuitive/more like an actual granulator (overlap should be grain frequency/grains per second, window_size should be in seconds)
#3 add pitch changing
#2 implement randomness parameters (% randomness)

def granulate_crosssim(track1, track2, sim_mat, sr, grain_frac, grains_per_window, overlap, output_size, window_type = 'no window',
    branch = 0.3, thresh = 0.8, jump = 0.6, breakout = 1):
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
    #track1 is always the longer track
    if track1.size <= track2.size:
        temp = track1
        track1 = track2
        track2 = temp

    #similarity matrix setup#
    #track2len = min(sim_mat.size[0], sim_mat.size[1])
    #track1len = max(sim_mat.size[0], sim_mat.size[1])

    feat_index_short = index_feature_vectors(sim_mat.shape[1], track2.size)
    feat_index_long = index_feature_vectors(sim_mat.shape[0], track1.size)

    # print "track1 size: ", track1.size
    # print "track2 size: ", track2.size
    #print sim_mat.shape
    #potentially create a new order every iteration
    order_short = np.random.randint(sim_mat.shape[1], size=sim_mat.shape[1])
    #print order_short.size
    order_long = np.random.randint(sim_mat.shape[0], size=sim_mat.shape[0])
    #print order_long.size
    #eventually these will be user defined

    #END#

    output = np.array([0])
    output_len = output_size * sr
    nbreak = 0 #A counter for how many times breakout was called

    if grain_frac > 0:
        grain_size = int(sr * grain_frac)
        window_size = grain_size * grains_per_window
    else:
        grain_size = int(sr * 0.05)
        window_size = grain_size * grains_per_window

    if window_size > track2.size:
        window_size = track2.size/grain_size
        print "window size too big, setting to: ", window_size


    if window_type is 'no window':
        window = one
    elif window_type is 'hann':
        window = scipy.signal.hann
    elif window_type is 'triangle':
        window = scipy.signal.triang
    elif window_type is 'tukey':
        window = scipy.signal.tukey

    #x = 0
    x = np.random.randint(0, track1.size/2)
    begin = x

    end = begin + output_len

    music = track1
    feat_index = feat_index_long
    order = order_long
    track = 1

    #music = track2
    #feat_index = feat_index_short
    #order = order_short
    #track = 2


    while output.size < output_len:
        #print "track: ", track
        if (x + window_size) >= music.size:
            x = np.random.randint(0, music.size/2)
        #print "output size: ", output.size
        if grain_frac is 0:
            grain_size = int(sr*((0.1 - 0.01) * np.random.random())) #+ 0.01
            if grain_size >= output.size and x != begin:
                grain_size = output.size

        start = np.random.randint(x, (x+(window_size - grain_size)))
        stop = start + grain_size
        #print start, stop, music[start:stop].size
        grain = music[start:stop] * window(grain_size)


        #print "grain size: ", grain.size

        if x is begin:
            output = np.append(output, grain )
        else:
            if overlap is 0:
                postpad = int(grain_size*((0.1 - 0.01) * np.random.random()))
            else:
                postpad = int(grain_size * (overlap))
            #print output.size
            output = np.lib.pad(output, (0,postpad), 'constant', constant_values=(0, 0))
            prepad = output.size - grain_size
            grain = np.lib.pad(grain, (prepad,0), 'constant', constant_values=(0, 0))

            output = output + grain

        #if np.random.random() > branch:
        #    vec = np.searchsorted(feat_index, x) - 1
        #    for index in order:
        #        if sim_mat[vec][index] > thresh and index is not vec:
        #            if feat_index[index] < (music.size - window_size):
        #                x = feat_index[index]
        #                break

        #our issue is that we are trying to jump within a song as well as between two songs
        #really it should only jump between one song or another.
        #if we want to both jump within a song and between two songs, we need to pass a self sim for each song as well
        #elif np.random.random() > jump:
            #potentially create a new order every iteration

        if np.random.random() > jump:
            if track is 1:
                music = track2
                track = 2
                feat_index = index_feature_vectors(sim_mat.shape[1], track2.size)
                order = np.random.randint(sim_mat.shape[1], size=sim_mat.shape[1])
            else:
                music = track1
                track = 1
                feat_index = index_feature_vectors(sim_mat.shape[0], track1.size)
                order = np.random.randint(sim_mat.shape[0], size=sim_mat.shape[0])
            vec = np.searchsorted(feat_index, x) - 1
            #print "feat index size: ", feat_index.size, " vec: ", vec
            #print "order size: ", order.size
            #print "track is: ", track
            for index in order:
                if track is 2:
                    x = vec
                    y = index
                else:
                    x = index
                    y = vec
                # print "x: ", x, " y: ", y
                # print "matrix shape: ", sim_mat.shape
                if sim_mat[x][y] > thresh and index is not vec:
                    if feat_index[y] < (music.size - window_size):
                        x = feat_index[y]
                        #take the next grain from the nearest 10 feature vectors
                        if y < feat_index.size - 5 and y > 5:
                            x = np.random.randint(feat_index[y-5], feat_index[y+5])
                        else:
                            x = np.random.randint(feat_index[0], feat_index[feat_index.size-1])
                        break

        #break out of the same feature we are stuck in
        if np.random.random() > breakout:
            nbreak +=1
            x = np.random.randint(0, music.size)
        x += grain_size


    print "Breakout called", nbreak, "times"
    return output

def normalize_pair(song1, song2):
    '''
    INPUT:
        song1, song2: the two signals you wish to be normalized
    OUTPUT:
        norm1, norm2: the two input track normalized based on the smaller max amplitude of the two tracks
    '''
    max1 = np.amax(song1)
    max2 = np.amax(song2)

    norm = min(max1, max2)

    norm1 = song1 / norm
    norm2 = song2 / norm

    return norm1, norm2
#@TODO
#When we turn this into an object, just give it a file and it will default all the params so the file just plays normally
#i.e. no overlap, grain size is some preset, window size is preset, window is 1, all randomness set to zero.
#basically it will just tack on unwindowed grains in sequential order so it plays normally. then we can fuck with the params later

if __name__ == "__main__":

    print "This is a demo of the granulate function. \nIt generates a 30s output file named grantest.wav. \nIt uses 2ms grains, a selection range of 1000 grains, and a Tukey window."
    path = raw_input("Please enter your .wav file name/path: ")

    music, sr = librosa.load(path)

    test = granulate(music, sr, 0.02, 1000, 0.5, 30, 'tukey')

    librosa.output.write_wav('grantest.wav', test, sr)
