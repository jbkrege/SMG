from simmatrix import *
from granulate import *

class Granulator:
	"""
	The SMG granulator class

	__init__ perams:
	sources: paths to the source files
	set source2 to zero if using self simmilarity
	
	features: 0 = chroma, 1 = chepstra
	"""
	distance_metric = "euclidean"
	destination = '../SMG_Output_Files/_output.wav'
	branch = .5
	thresh = .8
	jump = .6
	breakout = 1
	level1 = 1
	level2 = 1

	def __init__(self, source1, source2, features = 0, grain_len = .1, grains_per_window = 50, overlap = .5, output_size = 30, window_type = "tukey"):
		self.source1 = source1
		self.source2 = source2
		self.load(source1, source2)
		print "Creating feature vectors"
		self.features = features
		self.setFeatures()
		self.grain_len = grain_len
		self.grains_per_window = grains_per_window
		self.overlap = overlap
		self.output_size = output_size
		self.window_type = window_type
		print "Granulator initialized and ready to rock."

	def man(self):
		print "run: Makes output file and saves it at destination"
		print "Print: Prints the current state of all vars"
		print "load: takes two source files and precomputes necessary files"
		print "setGrainlen"
		print "setWindowlen"
		print "setWindowtype"
		print "setSource1"
		print "setSource2"
		print "setOverlap"
		print "setDestination"
		print "setBranch"
		print "setThresh"
		print "setJump"
		print "setBreakout"
		print "setDistance"
		print "setLevel1. A multiplier on source 1's amplitudes. For use with mixing"
		print "setLevel2"

	def setGrainlen(self, new):
		self.grain_len = new
	def setWindowlen(self, new):
		self.grains_per_window = new
	def setWindowtype(self, new):
		self.window_type = new
	def setSource1(self, new):
		self.load(new, self.source2)
		self.setFeatures()
	def setSource2(self, new):
		self.load( self.source1, new)
		self.setFeatures()
	def setOverlap(self, new):
		self.overlap = new
	def setDestination(self, new):
		self.destination = new
	def setBranch(self, new):
		self.branch = new
	def setThresh(self, new):
		self.thresh = new
	def setJump(self, new):
		self.jump = new
	def setBreakout(self, new):
		self.breakout = new
	def setDistance(self, distancem):
		Granulator.distance_metric = distancem
	def setLevel1(self, new):
		self.level1 = new
	def setLevel2(self, new):
		self.level2 = new

	def Print(self):
		print "Source1: ", self.source1
		print "Source2: ", self.source2
		print "Destination: ",self.destination
		if self.features:
			print "Features: Chepstra"
		else:
			print "Features: Chroma"
		print "Distance_measure: ", self.distance_metric
		print "Grain Length: ",self.grain_len
		print "Grains per window: ", self.grains_per_window
		print "Window type: ", self.window_type
		print "Overlap: ", self.overlap
		print "Branch: ", self.branch
		print "Similarity threshold: ", self.thresh
		print "Jumping probability: ", self.jump
		print "Breakout: ", self.breakout
		print "Level 1: ", self.level1
		print "Level 2:", self.level2

	def run(self, output_file = 'none'):
		if output_file != 'none':
			self.destination = output_file
		if self.source2:
			ret = granulate_crosssim(self.song1*self.level1, self.song2*self.level2,
			 self.crosssim, self.sr1, self.grain_len,
			 self.grains_per_window, self.overlap, self.output_size, self.window_type,
			 self.branch, self.thresh, self.jump, self.breakout)
			librosa.output.write_wav(str(self.destination), ret, self.sr1)
		else: 
			print "selfsim not yet implimented"
		print "File saved to ", self.destination
		

	def load(self, source1, source2):
		print "Loading from source files"
		song1, sr1 = librosa.load(str(source1))
		if (source2 != 0):
			song2, sr2 = librosa.load(str(source2))
		else:
			song2, sr2 = 0
		# Swap if the second source is longer than the first
		if song2.shape[0] > song1.shape[0]:
			temp = song1
			temp2 = sr1
			temp3 = source1
			song1 = song2
			sr1 = sr2
			source1 = source2
			song2 = temp
			sr2 = temp2
			source2 = temp3
		if (sr1 != sr2) and (sr2 != 0):
			print "WARNING: Sample rates do not match"
		self.song1 = song1
		self.sr1 = sr1
		self.source1 = source1
		self.song2 = song2
		self.sr2 = sr2
		self.source2 = source2

	def setFeatures(self, nfeatures = 'none'):
		if nfeatures == 'none':
			nfeatures = self.features
		if nfeatures:
			self.features = 1
			self.f1 = librosa.feature.mfcc(self.song1, self.sr1)
			if self.source2:
				self.f2 = librosa.feature.mfcc(self.song2, self.sr2)
		else:
			self.features = 0
			self.f1 = librosa.feature.chroma_stft(self.song1, self.sr1)
			if self.source2:
				self.f2 = librosa.feature.chroma_stft(self.song2, self.sr2)
		if self.source2:
			print "Constructing Cross-Similarity Matrix"
			self.crosssim = cross_sim_matrix(self.f1,self.f2,self.sr1, hop_length = 0, distance_metric = self.distance_metric, display = False)
		else:
			print "Impliment Self-Similarity Matrix"


