#!/usr/local/bin/python

import sys
import scipy.signal
import scipy.io.wavfile
import numpy
import matplotlib.pyplot
from scipy.misc import imsave

sps,aud = scipy.io.wavfile.read(sys.argv[1])


aumono= aud.reshape(-1,order='F')

f,t,sxx=scipy.signal.spectrogram(aumono,sps,nperseg=1024)



print f.shape
print t.shape
print sxx.shape

dx=t.__len__()
dy=f.__len__()

print dx,dy

syy = numpy.rot90(sxx)

scipy.misc.imsave("test.png",syy)

#for freq in t:
	#print freq,

#print

am=[]
for xx in syy:
	mm=xx.max()
	count=0
	am.append(mm)
	for x in xx:
		if (x==mm):
			print mm,f[count]
		
		count+=1


matplotlib.pyplot.plot(am,am)
matplotlib.pyplot.show()
