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
	else:
		samples, = samples


	print("SPS: " + str(sps))
	print("Channels: " + str(chan))
	print("Samples: " + str(samples))

	ss = samples

	xf = numpy.linspace(0,sps/2,ss//2)

		
	caud = aud.transpose()
        
	if chan == 1:
		caud = numpy.array([caud])


	for a in caud:
		sff = scipy.fft.fft(a)

	#for pp in range(xf.size):
	#	print(xf[pp],numpy.abs(sff[pp]))

		pt.semilogy(xf,numpy.abs(sff[0:ss//2]))

	pt.show()
