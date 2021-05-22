#!/usr/local/bin/python3

import sys
from scipy import interpolate
import scipy.io.wavfile

import scipy.signal as rs
import numpy as np

import matplotlib.pyplot as pt

x_points=[]
y_points=[]
with  open(sys.argv[1], 'r', encoding='utf-8') as infile:
	for line in infile:
		newline = line.rstrip() 
		la=newline.split()
		x_points.append(la[0])
		y_points.append(la[1])
		

tck = interpolate.splrep(x_points, y_points)
pts=[]
for x in range (1704):
	pts.append(  interpolate.splev(x, tck))

dt=np.array(pts)
#dt = np.absolute(np.gradient(don)) 


#pt.plot(dt)
#pt.show()


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

outs =int( np.round( sps * frames / frame_rate))

rd= rs.resample(dt,outs)
rd *= 32767
scipy.io.wavfile.write(sys.argv[1]+".fm.wav", sps, rd.astype(np.int16))
