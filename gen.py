#!/usr/bin/python

import numpy as np
import scipy.io.wavfile as wv
import scipy.signal

duration = 20.0
fs = 44100.0
samples = int(fs*duration)
t = np.arange(samples) / fs

#print t

#signal = scipy.signal.chirp(t, 50.0, t[-1], 1050.0)
signal =  np.sin(2.0*np.pi * 200 *t)

signal *= (1.0 + 0.5 * np.sin(2.0*np.pi*1.0*t) )

wv.write("test.wav",44100,signal)
