#!/usr/local/bin/python3

import math
#import pysig as ps
from pysig import *

mod = Linear([0,300],[0.666,3])
lcar = Sine(Add(570,Negative(mod)))
rcar = Div(Add(Sine(330),Add(Sine(Add(570,mod)),Sine(1470))),3)

bmod = Sine(mod)
rmod = Scale(bmod,outscale=[0,1])
lmod = Scale(Hilbert(bmod),outscale=[0,1])

lsig = AM(lmod,lcar)
rsig = AM(rmod,rcar)
env = Linear([0,2,298,300],[0,1,1,0])
lenv = AM(env, lsig)
renv = AM(env, rsig)

write(lenv,renv,sps=22050,name="mas3.wav")
