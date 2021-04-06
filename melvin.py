#!/usr/local/bin/python3

import math
import pysig as ps

lcar = ps.Square(600)
rcar = ps.Sawtooth(600)

mod = ps.Scale(ps.Sine(10),outscale=[ps.DB(-9),ps.DB(-6)])
amp = ps.DC(ps.DB(-6))

lmod = ps.AM(mod,lcar)
rmod = ps.AM(mod,rcar)
lca = ps.AM(amp,lcar)
rca = ps.AM(amp,rcar)

ref = ps.Linear([0,300],[0.1,10])
trans = ps.Sine(ref)

lmt = ps.Mplex(trans,lmod,lca)
rmt = ps.Mplex(trans,rca,rmod)

env = ps.Linear([0,2,300],[ps.DB(-96),ps.DB(-3),ps.DB(-3)])

lenv = ps.AM(env,lmt)
renv = ps.AM(env,rmt)

ps.write(lenv,renv,sps=22050,name="melvin3.wav")