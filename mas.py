#!/usr/local/bin/python3

import math
<<<<<<< HEAD
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
=======
import pysig as ps

mod = ps.Linear([0,300],[0.666,3])
lcar = ps.Sine(ps.Add(570,ps.Negative(mod)))
rcar = ps.Div(ps.Add(ps.Sine(330),ps.Add(ps.Sine(ps.Add(570,mod)),ps.Sine(1470))),3)

bmod = ps.Sine(mod)
rmod = ps.Scale(bmod,outscale=[0,1])
lmod = ps.Scale(ps.Hilbert(bmod),outscale=[0,1])

lsig = ps.AM(lmod ,lcar)
rsig = ps.AM(rmod,rcar)
env = ps.Linear([0,2,300],[0,ps.DB(-3),ps.DB(-3)])
lenv = ps.AM(env, lsig)
renv = ps.AM(env , rsig)


ps.write(lenv,renv,sps=22050,name="mas3.wav")
>>>>>>> c2ed75a8440e3f98753a7ef7f37ebb0b720606c0
