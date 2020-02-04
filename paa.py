#!/usr/local/bin/python3

from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction

import matplotlib.pyplot as plt
import sys

sys.argv.pop(0)

for fn in sys.argv:
	print(fn)
	[Fs, X] = audioBasicIO.readAudioFile (fn)


	F,f_names=audioFeatureExtraction.stFeatureExtraction(X, Fs, 0.05 * Fs, 0.025 * Fs)
	plt.subplot(2,1,1); 
	plt.plot(F[3,:]); 
	plt.xlabel("frame"); 
	plt.ylabel(f_names[3]);
	plt.subplot(2,1,2); 
	plt.plot(F[7,:]); 
	plt.xlabel("frame"); 
	plt.ylabel(f_names[7]);
	plt.show()
