#!/usr/local/bin/python3

import numpy as np
import scipy.io.wavfile as wv
import scipy.signal
import argparse

def waveread(fn):
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

	return sps,caud


#duration = 20.0
freq=440
#fs = 44100.0

parser = argparse.ArgumentParser(description='mod a wave signal.')
parser.add_argument("files", nargs='+', help='wave files')
parser.add_argument("-c", "--frequency", dest="freq", action="store", help="Carrier Frequency Hz")
parser.add_argument("-a", "--am", dest="am", action='store_true', help="am modulation")
parser.add_argument("-f", "--fm", dest="fm", action='store_true', help="fm modulation")
parser.add_argument("-i","--invertfm",dest="invertfm", action="store_true", help="invert FM modulation")
parser.add_argument("-d", "--depth", dest="depth", action="store", help="fm modulation depth hz")
parser.add_argument("-C", "--channel", dest="channel", action='store', help="decode only channel C")
parser.add_argument("-m", "--modulate", dest="modfile", action='store', help="Modulate this file")
args = parser.parse_args()

if (args.freq and args.modfile):
	print("cannot modulate both carrier and file")
	exit(1)

#if (args.modfile):


for fn in args.files:

	sps,caud = waveread(fn)

	samples = caud[0].__len__()

	print(samples)

	maud=""
	if (args.modfile):
		msps,maud = waveread(args.modfile)
	
	# want a single scale for both channels
	autoscmin=0
	autoscmax=65536.0
	scale = 1.0 
	if (args.depth):
		autoscmin =int(caud.min())
		autoscmax =int(caud.max())
		print(autoscmin,autoscmax)
		scale = float(args.depth) / (autoscmax - autoscmin)
		print ("FM Scale", scale)
	
	if (args.channel):
		selchan = int(args.channel)
		caud=np.array([caud[selchan]])
		if (args.modfile):
			maud = np.array([maud[selchan]])
	#caud = np.double(aud.transpose())
	naud = []

	for ch in range(caud.__len__()):

		ad = np.double(caud[ch])
		if (args.modfile):
			signal  = np.zeros(ad.shape)

			mchan,msamp = maud.shape
			if ch >= mchan:
				sigwave = np.double(maud[mchan-1])  # ill assume this is mono, so repeats the max channel
			else:
				sigwave = np.double(maud[ch])
			#print(sigwave.shape)
			signal[:sigwave.shape[0]] = sigwave[:samples]
			max = signal.max()
			#print (max)
			signal /= max
			#signal = signal[:samples]
			# sorry no FM modulation of a signal... yet?
		elif (args.fm):
			fd=np.array(ad)

		#	autoscmin = 0 #ad.min()
		#	autoscmax = 0 #ad.max()
	
			# want a single scale for both channels
			#scale = float(args.depth) / (autoscmax - autoscmin)
			#print ("FM Scale", scale)
			fd -= autoscmin
			fd -= (autoscmax - autoscmin) / 2;
			fd *= scale
			if (args.invertfm):
				fd = -fd  # lower frequencies are more intense
			if (args.freq):
				fd += float(args.freq) 

			iaud = fd.cumsum() / (sps * 1.0) # funky

			signal =  np.sin(np.pi * iaud)  # or read from modfile
		else:
			# only AM modulation; create a carrier
			t = np.arange(samples) / ( sps * 1.0 )
			# what about other types of generated signals, square anyone?
			signal =  np.sin(2.0*np.pi * float(args.freq) *t) # or read from modfile
			#signal += np.sin(6.0*np.pi * float(args.freq) *t) # or read from modfile
			#signal += np.sin(10.0*np.pi * float(args.freq) *t) # or read from modfile



		print (ad)
		print (signal)

		if (args.am):
			#ad += 32768
			#ad /= 32768
			# had it wrong, hmm unsigned, the format must support both signed an unsigned
			ad /= 65535

			#print (caud)
			#print (signal)
			print ("AM Modulate")
			signal *= ad

		naud.append(signal)

	mtype = ""
	if (args.fm):
			mtype = "fm"
	if (args.am):
			mtype += "am"

	npaud = np.array(naud)
	if (args.freq):
		nfn = fn.replace(".wav","."+mtype+"-"+args.freq+".wav")
	else:
		nfn = fn.replace(".wav","."+mtype+"-0"+".wav")

	wv.write(nfn,sps,npaud.transpose())
