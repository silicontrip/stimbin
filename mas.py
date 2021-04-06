#!/usr/local/bin/python3

import math
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
