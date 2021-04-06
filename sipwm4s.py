#!/usr/local/bin/python3
import math
import pysig as ps
from pysig import DB
#import matplotlib.pyplot as pt
#import numpy

env = ps.Linear([0,2,60,300],[DB(-96),DB(-7),DB(-5),DB(-5)])

mf=ps.Linear([0,300],[0.25,4])
simr=ps.Sine(mf)
siml=ps.Hilbert(simr)

# I thought that this should be sine ?
#ramp = ps.Linear([0,30,60,90,120,150,180,210,240,270,300],[0,1,0,1,0,1,0,1,0,1,0])  
#lamp = ps.Hilbert(ramp)
ampr = ps.Square(440,duty=ps.Scale(simr))
ampl = ps.Square(440,duty=ps.Scale(siml))
renvcar = ps.AM(env,ampr)
lenvcar = ps.AM(env,ampl)

ps.write(lenvcar,right=renvcar,sps=22050,name="sipwm4s.wav")

