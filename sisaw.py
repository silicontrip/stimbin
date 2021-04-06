#!/usr/local/bin/python3
import pysig as ps
from pysig import DB
#import matplotlib.pyplot as pt
#import numpy

v = ps.Linear([0,10],[1,8])
spd = ps.Linear([0,10],[1,4])
wv = ps.Scale(ps.Sawtooth(v),[-1,1],[1,10000000000])
gen = ps.Scale(ps.Log(wv),[0,10],[0,1])
car = ps.Sine(ps.Scale(ps.Sine(spd), [-1,1],[400,800]))

encar = ps.AM(car,gen)

#ps.plotsig(encar,65536)
ps.write(encar,name="silogsweep.wav")
