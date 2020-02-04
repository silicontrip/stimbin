#!/usr/local/bin/python3
import math
import pysig as ps
#import matplotlib.pyplot as pt
#import numpy

carrier = ps.Sine(600)
carrier2 = ps.Square(600)

ramp = ps.Linear([0,300],[1,4])  # i don't know why this value needs to be halved. (because AM modulated is ABS(sine) therefore doubling the Hz
amp = ps.Sine(ramp)
iamp = ps.Negative(amp)
osc = ps.Mplex(amp,carrier,carrier2)
iosc = ps.Mplex(iamp,carrier,carrier2)

env = ps.Linear([0,2,60,300],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-5)])
envcar = ps.AM(env,osc)
ienvcar = ps.AM(env,iosc)


ps.writestereo(envcar,ienvcar,22050,"sisq-mplex.wav")
#ps.writemono(envcar,22050,"sisq-mplex.wav")

