#!/usr/local/bin/python3
import pysig as ps
#import matplotlib.pyplot as pt
import numpy

ramp = numpy.linspace(1,8,150)
rr = ps.Linear([0,2.5,3],[600,100,100])
signal = ps.Square(rr,amplitude=ps.DB(-1))

for x in ramp:
	rr = ps.Linear([0,2.5/x,3/x],[600,100,100])
	sig1 = ps.Square(rr,amplitude=ps.DB(-1))
	signal = ps.Cat(signal,sig1)

ps.writemono(signal,22050,"stim.wav")
