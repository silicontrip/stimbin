#!/usr/local/bin/python

import sys
import scipy.signal
import scipy.io.wavfile
import numpy
import argparse

parser = argparse.ArgumentParser(description='demodulate a wave signal.')
parser.add_argument("files", nargs='+', help='wave files')
parser.add_argument("-a", "--am", dest="am", action='store_true', help="am demodulation")
parser.add_argument("-f", "--fm", dest="fm", action='store_true', help="fm demodulation")

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
	
	
		
		# am
		#print "abs"
		if (args.am):
			sigmod = numpy.abs(sigcmplx)
			naud.append(sigmod)

		
		# fm
	# calculate carrier frequency
		if (args.fm):
			scale = 32768.0 / numpy.pi
			sigfreq = numpy.diff(numpy.unwrap(numpy.angle(sigcmplx))) * scale
			naud.append(sigfreq)
			
		# /(2*numpy.pi) * sps
	# assuming am constant carrier
		#sigfreq.sort()
	#median frequency
		#print str(sigfreq[sigfreq.__len__() / 2] ) + " Hz"
	
		#print min(sigmod) , max(sigmod)
		#print sigmod
	
	
		print naud

	nfn=""	
	if (args.fm):
		nfn = fn.replace(".wav",".fm.wav")
	if (args.am):
		nfn = fn.replace(".wav",".am.wav")
	
	if (nfn):
		npaud = numpy.array(naud)
		wavout=numpy.array(npaud.transpose(),dtype='int16')
		scipy.io.wavfile.write(nfn, sps, wavout)
	
