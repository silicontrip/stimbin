#!/usr/bin/python

import numpy as np
import scipy.io.wavfile as wv
import scipy.signal
import argparse

import matplotlib.pyplot as mpl

#duration = 20.0
freq=440
#fs = 44100.0

parser = argparse.ArgumentParser(description='mod a wave signal.')
parser.add_argument("files", nargs='+', help='wave files')
parser.add_argument("-c", "--frequency", dest="freq", action="store", help="Centre Frequency Hz")
parser.add_argument("-d", "--depth", dest="depth", action="store", help="modulation depth hz")
parser.add_argument("-C", "--channel", dest="channel", action='store', help="decode only channel C")

args = parser.parse_args()

for fn in args.files:
	sps,aud = wv.read(fn)

	samples=aud.shape

	print (samples)

	chan = 1
	if (len(samples)>1):
		(samples,chan) = samples
	else:
		(samples,) = samples
	
	print ("SPS: " + str(sps))
	print ("Channels: " + str(chan))
	print ("Samples: " + str(samples))
	
	#print aud
	
	caud = aud.transpose()
	
	if chan == 1:
		caud = np.array([caud])
	
	if (args.channel):
		selchan = int(args.channel)
		#print caud[selchan]
		caud=np.array([caud[selchan]])
	
	#caud = np.double(aud.transpose())
	naud = []
	for a in caud:

		ad = np.double(a)
	
		autoscmin = ad.min()
		autoscmax = ad.max()
	
		scale = float(args.depth) / (autoscmax - autoscmin)
		print ("Scale ", scale)
		ad -= autoscmin
		ad *= scale
		ad = -ad 
		ad += float(args.freq)
		#ad = -caud  # because lower frequencies are more intense...
	
		iaud = ad.cumsum() / (sps * 1.0)
	
	#for c in caud:
		#mpl.plot(ad)
		#mpl.show()	
	
		signal =  np.sin(2 * np.pi *  iaud)  

#	print caud
		#print signal.min() , signal.max()
		naud.append(signal)
	#signal *= caud

	npaud = np.array(naud) 
	#print npaud.shape
	#wavout=np.array(npaud.transpose(),dtype='int16')
	#mpl.plot(naud)
	#mpl.show()
	nfn = fn.replace(".wav","."+args.freq+".wav")
	wv.write(nfn,sps,npaud.transpose())
