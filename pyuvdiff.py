#!/usr/local/bin/python3

import numpy as np
import matplotlib.pyplot as pt
import scipy.signal as rs
import scipy.io.wavfile
import sys

f=open(sys.argv[1])

pts=[]
for l in f:
	(fn,dd) = l.rstrip().split(' ')
	pts.append( float(dd))


dt=np.array(pts)
frames=len(dt)
minv = min(dt)
maxv = max(dt)
range=maxv-minv
dt -= minv
dt /= range
#dt -= 1.0
print (minv,maxv)

sps = 44100
frame_rate = 30000. / 1001.
frame_rate = 25.
outs =int( np.round( sps * frames / frame_rate))

rd= rs.resample(dt,outs)
rd *= 65535
scipy.io.wavfile.write(sys.argv[1]+".am.wav", sps, rd.astype(np.int16))

