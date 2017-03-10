# This line is a convenience to import most packages you'll need. You may need to import others (eg random and cmath)
import IPython, numpy as np, matplotlib.pyplot as plt, matplotlib, sklearn, librosa, cmath,math, scipy
from IPython.display import Audio
from IPython.display import HTML

# This line makes sure your plots happen IN the webpage you're building, instead of in separate windows.
#%matplotlib inline

def apply_style():
    """
	Useful styles for displaying graphs and audio elements.
	"""
    style = HTML("""
        <style>
            audio {
            width: 100% !important;
        }
        .output_png {
            text-align: center !important;
        }
        </style>
        """)
    IPython.display.display(style)

def audio(d, sr, ext = '.mp3'):
    """
	Embeds audio into notebook
	Parameters:
	   d: numpy array of audio data.
	   sr: sampling rate for the audio
	"""
    IPython.display.display(IPython.display.Audio(data=d, rate = sr))

#apply_style()

music, sr = librosa.load('music/call_me_maybe.wav')
hop_length = 1024
n_fft = 2048
stft = librosa.stft(music, hop_length = hop_length, n_fft = n_fft)
log_spectrogram = librosa.logamplitude(np.abs(stft**2), ref_power=np.max)
Audio(music, rate=sr)

plt.figure(figsize=(20, 4))
librosa.display.specshow(log_spectrogram, sr = sr, hop_length = hop_length, y_axis = 'log', x_axis = 'time')
plt.show()


print music.size, sr

siglen = music.size

test_siglen = siglen/5

grain_size = sr/100

start = 0#np.random.randint(0, (music.size - grain_size))

granulated = np.array([0])

#envelope range
grain_range = grain_size*500

#actual envelope
#window = scipy.signal.hann(grain_size)
#window = scipy.signal.triang(grain_size)
window = 1

#timestretching
gap_size = 0#500
gap = np.zeros(gap_size)

#window = scipy.signal.hann(grain_size)
#window = scipy.signal.triang(grain_size)
#window = 1
n=1
x=0
w=80

mod = False

while x < test_siglen:
    #modulating grain size will take a little thinking, but not hard
    '''
    if not mod:
        if n < 100:
            n+=1
        else:
            mod = True
    else:
        if n > 1:
            n-=1
        else:
            n+=1
            mod = False

    grain_size = sr/n
    grain_range = grain_size*w
    '''

    start = np.random.randint(x, (x+(grain_range - grain_size)))
    stop = start + grain_size
    window = scipy.signal.triang(grain_size)
    grain = music[start:stop] * window

    #modulate the timestretch sort of

    #gap_size -= 100
    #if gap_size > 0:
    #    gap = np.zeros(gap_size)


    granulated = np.append(granulated, grain )
    granulated = np.append(granulated, gap)
    x += grain_size

Audio(granulated, rate=sr)
