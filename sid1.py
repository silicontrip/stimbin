#!/usr/local/bin/python3
import math
import pysig as ps
import matplotlib.pyplot as pt
import numpy

dp=ps.Linear([0,1],[0,2*numpy.pi])
di=ps.Linear([0,1],[0,10])
carrier = ps.Sine(50,distortion=1.1,distortionphase=dp,duration=1)

ps.plotsig(carrier,5120)


