#!/usr/local/bin/python3

import matplotlib.pyplot as pt
import scipy.io.wavfile as wv
import argparse
import numpy as np


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

parser = argparse.ArgumentParser(description='mod a wave signal.')
parser.add_argument("files", nargs='+', help='wave files')
parser.add_argument("-o", "--order", dest="order", action='store',help="select polynomial order")
parser.add_argument("-C", "--channel", dest="channel", action='store', help="decode only channel C")

args = parser.parse_args()

for fn in args.files:
	sps,caud = waveread(fn)

	print(sps)
	print(caud)

	for a in caud:
		pos= a[17:]+32764

	#	pt.plot(pos)
	#	pt.show()

		mx = pos.max()
		mn = pos.min()

		print(mn,mx)

		pos = pos /  mx

		xv = np.arange(pos.__len__()) / pos.__len__()
		pll = np.polyfit(xv,pos,int(args.order))
		ply= np.poly1d(pll)
		
		print(ply)

		yv=ply(xv)
		pt.plot(pos)
		pt.plot(yv)
		pt.show()
		break

