#!/usr/local/bin/python3
import math
import pysig as ps
#import matplotlib.pyplot as pt
#import numpy


transition=ps.Linear([0,300],[0.1,4])

mod = ps.Sine(transition)
osc = ps.Random(777)


mosc = ps.AM(osc,mod)
rosc = ps.Hilbert(mosc)

env = ps.Linear([0,2,60,300],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-5)])
ienvcar = ps.AM(env,mosc)
renvcar = ps.AM(env,rosc)

ps.write(ienvcar,right=renvcar,sps=22050,name="rand-777.wav")

