#!/usr/local/bin/python3

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
parser.add_argument("-a", "--am", dest="am", action='store_true', help="am modulation")
parser.add_argument("-f", "--fm", dest="fm", action='store_true', help="fm modulation")
parser.add_argument("-d", "--depth", dest="depth", action="store", help="modulation depth hz")
parser.add_argument("-C", "--channel", dest="channel", action='store', help="decode only channel C")

args = parser.parse_args()

for fn in args.files:
	sps,aud = wv.read(fn)

	samples=aud.shape

	chan = 1
	if (len(samples)>1):
		(samples,chan) = samples
	else:
		(samples,) = samples
	
	print ("SPS: " + str(sps))
	print ("Channels: " + str(chan))
	print ("Samples: " + str(samples))
		
	caud = aud.transpose()
	
	if chan == 1:
		caud = np.array([caud])
	
	if (args.channel):
		selchan = int(args.channel)
		caud=np.array([caud[selchan]])
	
	#caud = np.double(aud.transpose())
	naud = []

	for a in caud:
		ad = np.double(a)

		if (args.fm):
			autoscmin = ad.min()
			autoscmax = ad.max()
	
			scale = float(args.depth) / (autoscmax - autoscmin)
			print ("FM Scale", scale)
			ad -= autoscmin
			ad *= scale
			ad = -ad  # lower frequencies are more intense
			ad += float(args.freq)

			iaud = ad.cumsum() / (sps * 1.0)
			signal =  np.sin(2 * np.pi *  iaud) 
		else:
			# only AM modulationr; create a carrier
			t = np.arange(samples) / ( sps * 1.0 )
			signal =  np.sin(2.0*np.pi * float(args.freq) *t)

		if (args.am):
			ad += 32768
			ad /= 32768

			#print (caud)
			#print (signal)

			signal *= ad

		naud.append(signal)

	mtype = ""
	if (args.fm):
			mtype = "fm"
	if (args.am):
			mtype += "am"
			
	npaud = np.array(naud) 
	nfn = fn.replace(".wav","."+mtype+"-"+args.freq+".wav")
	wv.write(nfn,sps,npaud.transpose())
