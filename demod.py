#!/usr/local/bin/python3

import sys
import scipy.signal
import scipy.io.wavfile
import scipy.fftpack
import numpy

import argparse

parser = argparse.ArgumentParser(description='demodulate a wave signal.')
parser.add_argument("files", nargs='+', help='wave files')
parser.add_argument("-a", "--am", dest="am", action='store_true', help="am demodulation")
parser.add_argument("-f", "--fm", dest="fm", action='store_true', help="fm demodulation")
parser.add_argument("-C", "--channel", dest="channel", action='store', help="decode only channel C")
parser.add_argument("-V", "--volume", dest="volume", action='store', help="set volume attenuation")
parser.add_argument("-r","--pre", dest="prefilter",action="store", help="pre-filter signal")
parser.add_argument("-p","--post", dest="postfilter",action="store", help="post-filter signal")

args = parser.parse_args()

for fn in args.files:
	# aud, sps= lr.load(fn) # this resamples to 22,050 and single channel
	# unless overridden, I want to preserve sps and channels.
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
	invert=False
	for a in caud:
		print (a)
	
		if (args.prefilter):
			lh = args.prefilter.split("-")
			print (lh)
			low = int(lh[0]) / nyq
			high = int(lh[1]) / nyq
			bb, ba = scipy.signal.butter(10,[low,high], btype='band')
			a = scipy.signal.lfilter(bb,ba,a)
			

			print(a)
		print("hilbert")
	#print "hilbert"
		sigcmplx = scipy.signal.hilbert(a)
		print(sigcmplx)
		# am
		print("am")
		if (args.am):
			if invert:
				sig = - numpy.abs(sigcmplx)
			else:
				sig = numpy.abs(sigcmplx) 
				#naud.append(sigmod)
			invert=True
		
		print("fm")
	# calculate carrier frequency
		if (args.fm):
			scale = 32768.0 / numpy.pi
			sig = numpy.diff(numpy.unwrap(numpy.angle(sigcmplx))) * scale
			#naud.append(sigfreq)
			
            
		if (args.volume):
			sig = sig * float(args.volume) / 100.0 
		# /(2*numpy.pi) * sps
	# assuming am constant carrier
		#sigfreq.sort()
	#median frequency
		#print str(sigfreq[sigfreq.__len__() / 2] ) + " Hz"
	
		#print min(sigmod) , max(sigmod)
		print (sig)
	
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

	nfn=""	
	stna = fn.split('.')
	# blindly slice off the last 4 characters
	if (args.fm):
		stna[-1] = "dfm"+ch+".wav"
		nfn = ".".join(stna)
	if (args.am):
		stna[-1] = "dam"+ch+".wav"
		nfn = ".".join(stna)


	
	if (nfn):
		print("Writing " + nfn + "...")
		npaud = numpy.array(naud)
		wavout=numpy.array(npaud.transpose(),dtype='int16')
		scipy.io.wavfile.write(nfn, sps, wavout)
	
