#!/usr/local/bin/python3

import sys
import scipy.signal
import scipy.io.wavfile
import numpy
import argparse

parser = argparse.ArgumentParser(description='demodulate a wave signal.')
parser.add_argument("files", nargs='+', help='wave files')
#parser.add_argument("-a", "--am", dest="am", action='store_true', help="am demodulation")
#parser.add_argument("-f", "--fm", dest="fm", action='store_true', help="fm demodulation")
parser.add_argument("-C", "--channel", dest="channel", action='store', help="decode only channel C")
parser.add_argument("-r","--pre", dest="prefilter",action="store", help="pre-filter signal")
parser.add_argument("-p","--post", dest="postfilter",action="store", help="post-filter signal")

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
	
	nyq= sps / 2.0

	
	#print aud
	
	caud = aud.transpose()
	
	if chan == 1:
		caud = numpy.array([caud])
	
	if (args.channel):
		selchan = int(args.channel)
		#print caud[selchan]
		caud=numpy.array([caud[selchan]])
	
	# print caud
	
	naud=[]
	for a in caud:
		print (a)
	
		if (args.prefilter):
			lh = args.prefilter.split("-")
			print (lh)
			low = int(lh[0]) / nyq
			high = int(lh[1]) / nyq
			bb, ba = scipy.signal.butter(6,[low,high], btype='band')
			a = scipy.signal.lfilter(bb,ba,a)
			
	#print "hilbert"
		sigcmplx = scipy.signal.hilbert(a)
		
		# am
		#print "abs"
		sig = numpy.abs(sigcmplx)
			#naud.append(sigmod)
		
		sig = ( a / sig ) * 32767.0


		if (args.postfilter):
			lh = args.postfilter.split("-")
			print(lh)
			low = float(lh[0]) / nyq
			high = float(lh[1]) / nyq
			cb, ca = scipy.signal.butter(3,[low,high], btype='band')
			sig = scipy.signal.lfilter(cb,ca,sig)

		naud.append(sig)

	
		print (naud)

	ch=""
	if (args.channel):
			ch=str(args.channel)

	nfn = fn.replace(".wav",".car"+ch+".wav")
	
	if (nfn):
		npaud = numpy.array(naud)
		wavout=numpy.array(npaud.transpose(),dtype='int16')
		scipy.io.wavfile.write(nfn, sps, wavout)
	
