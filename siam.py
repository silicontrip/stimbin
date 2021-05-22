#!/usr/local/bin/python3
import math
import pysig as ps
import matplotlib.pyplot as pt
import numpy

carrier = ps.Sine(948)

ramp = ps.Linear([0,300],[1,20])  # i don't know why this value needs to be halved. (because AM modulated is ABS(sine) therefore doubling the Hz
ramp2 = ps.Add(ps.AM(ps.Sine(ps.Linear([0,300],[1,4])),0.5),ramp)


pt.plot(ramp2.getsample(numpy.arange(0,300,0.01)))
pt.show()


amp = ps.Sine(ramp2)
iamp = ps.Sine(ramp2,phase=math.pi/2)
osc = ps.AM(amp,carrier)
iosc = ps.AM(iamp,carrier)

env = ps.Linear([0,2,60,300],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-5)])
envcar = ps.AM(env,osc)
ienvcar = ps.AM(env,iosc)


ps.writestereo(envcar,ienvcar,22050,"siam.wav")
#ps.writemono(envcar,22050,"sisq-mplex.wav")

