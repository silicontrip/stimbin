#!/usr/local/bin/python3

import sys
import scipy.signal
import scipy.io.wavfile
import imageio
import numpy
import argparse
import math


parser = argparse.ArgumentParser(description='demodulate a wave signal.')
parser.add_argument("files", nargs='+', help='wave files')

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



	imx = 1280
	imy = 720

	pa = numpy.zeros(shape=(imy,imx))

	caud = aud.transpose()
	scaley = (imy-1) / 65536
	scalex = (imx-1) / caud.size
	olx=0
	for ax in range(caud.size):
		px = caud[ax]+ 32768
		x = int(numpy.round(ax * scalex))
		y = int(numpy.round(px * scaley))
		
		pa[y][x] += 1	
		if not olx == x:
			print(x)
			olx=x
		

	gc = numpy.power(pa,0.45)
	imageio.imwrite(fn + ".png",gc)
