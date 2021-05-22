#!/usr/local/bin/python3
import math
import pysig as ps
#import matplotlib.pyplot as pt
#import numpy

env = ps.LinearEnvelope([0,2,60,300],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-5)])
carrier = ps.Sine(ps.DB(0),600,0)
carrier2 = ps.Sine(ps.DB(0),900,0)


ramp = ps.LinearEnvelope([0,300],[1,4])  # i don't know why this value needs to be halved.
amp = ps.Sine(ps.DB(0),ramp,ps.DC(0))
osc = ps.Mplex(amp,carrier,carrier2)

envcar = ps.AM(env,osc)
#amp2 = ps.AbsSig(ps.Sine(ps.DB(0),ramp,ps.DC(math.pi/2)))

#pt.plot(amp.getsample(numpy.arange(0,300,0.01)))
#pt.show()

#sigL=ps.AM(envcar,amp)
#sigR=ps.AM(envcar,amp2)

#sig = ps.Mplex(ps.Dur(ps.Square(ps.DB(0),ps.DC(1),ps.DC(0),ps.DC(0.1)),[0,300]),sigL,sigR)

ps.writemono(envcar,22050,"mplex.wav")

