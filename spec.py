#!/usr/local/bin/python3

import numpy as np
import matplotlib.pyplot as pt

import librosa as lr
import librosa.display as dp

import argparse

parser = argparse.ArgumentParser(description='demodulate a wave signal.')
parser.add_argument("files", nargs='+', help='wave files')
parser.add_argument("-a", "--am", dest="am", action='store_true', help="am demodulation")
parser.add_argument("-f", "--fm", dest="fm", action='store_true', help="fm demodulation")
parser.add_argument("-C", "--channel", dest="channel", action='store', help="decode only channel C")
parser.add_argument("-r","--pre", dest="prefilter",action="store", help="pre-filter signal")
parser.add_argument("-p","--post", dest="postfilter",action="store", help="post-filter signal")

args = parser.parse_args()

for fn in args.files:
	aud, sps= lr.load(fn)

	#dp.waveplot(aud,sr=sps)
	m = lr.stft(aud)
	db = lr.amplitude_to_db(abs(m), ref=np.max)

	dp.specshow(db, y_axis='mel', x_axis='time')

	pt.show()
