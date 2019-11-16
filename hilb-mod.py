#!/usr/local/bin/python

import sys
import scipy.signal
import scipy.io.wavfile
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
	
	print "SPS: " + str(sps)
	print "Channels: " + str(chan)
	print "Samples: " + str(samples)
	
	#print aud
	
	caud = aud.transpose()
	
	if chan == 1:
		caud = numpy.array([caud])
	
	#print caud

	
	naud=[]
	for a in caud:
	
		#print a
	
	#print "hilbert"
		sigcmplx = scipy.signal.hilbert(a)
		naud.append(sigcmplx.real)
		naud.append(sigcmplx.imag)

		print naud

	nfn = fn.replace(".wav",".hil.wav")

	
	if (nfn):
		npaud = numpy.array(naud)
		wavout=numpy.array(npaud.transpose(),dtype='int16')
		scipy.io.wavfile.write(nfn, sps, wavout)
	