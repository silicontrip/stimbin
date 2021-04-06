#!/usr/local/bin/python3

import sys
import scipy.signal
import scipy.io.wavfile
import scipy.fft
import matplotlib.pyplot as pt
import numpy
import argparse

parser = argparse.ArgumentParser(description='demodulate a wave signal.')
parser.add_argument("files", nargs='+', help='wave files')

args = parser.parse_args()

for fn in args.files:
	sps,aud = scipy.io.wavfile.read(fn)
	
	samples=aud.shape
	
	chan = 1
	if (len(samples)>1):
		(samples,chan) = samples

	print("SPS: " + str(sps))
	print("Channels: " + str(chan))
	print("Samples: " + str(samples))

	ss, = samples

	xf = numpy.linspace(0,sps/2,ss//2)

	caud = aud.transpose()
	if chan == 1:
		caud = numpy.array([caud])

	for a in caud:
		pt.grid()
		pt.plot(numpy.gradient(a))
		pt.show()
