#!/usr/bin/python

import numpy as np
import scipy.io.wavfile as wv
import scipy.signal
import argparse


#duration = 20.0
freq=440
#fs = 44100.0

parser = argparse.ArgumentParser(description='mod a wave signal.')
parser.add_argument("files", nargs='+', help='wave files')
parser.add_argument("-c", "--frequency", dest="freq", action="store", help="Carrier Frequency Hz")
args = parser.parse_args()

for fn in args.files:
	sps,aud = wv.read(fn)

	samples=aud.shape

	chan = 1
	if (len(samples)>1):
		(samples,chan) = samples
	else:
		(samples,) = samples
	
	print "SPS: " + str(sps)
	print "Channels: " + str(chan)
	print "Samples: " + str(samples)
	
	#print aud
	
	caud = np.double(aud.transpose())
	
	#samples = int(fs*duration)
	t = np.arange(samples) / ( sps * 1.0 )

	# print t
	#signal = scipy.signal.chirp(t, 50.0, t[-1], 1050.0)
	
	signal =  np.sin(2.0*np.pi * float(args.freq) *t) 

	caud += 32768
	caud /= 32768

	print caud
	print signal

	signal *= caud

	nfn = fn.replace(".wav","."+args.freq+".wav")
	wv.write(nfn,sps,signal)
