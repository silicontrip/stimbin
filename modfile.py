#!/usr/local/bin/python3

import numpy as np
import scipy.io.wavfile as wv
import scipy.signal
import argparse

import samplerate as sr

parser = argparse.ArgumentParser(description='mod a wave signal.')
parser.add_argument("files", nargs='+', help='wave files')

args = parser.parse_args()

mf = args.files.pop(0)

for fn in args.files:
	print("Mod" + fn + " with " + mf)
