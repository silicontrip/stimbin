#!/usr/local/bin/python3

import math
#import pysig as ps
from pysig import *


lcar = Square(600)
rcar = Sawtooth(600)

mod = Scale(Sine(10),outscale=[DB(-6),DB(-3)])
amp = DC(DB(-3))

lmod = AM(mod,lcar)
rmod = AM(mod,rcar)
lca = AM(amp,lcar)
rca = AM(amp,rcar)

env = Linear([0,2,298,300],[0,1,1,0])

#le = AM(env,lmod)
#re = AM(env,rmod)
#write(le,re,sps=11025,name="melvin-mod.wav")

#le = AM(env,lca)
#re = AM(env,rca)
#write(le,re,sps=11025,name="melvin-ca.wav")

#ref = Linear([0,300],[0.1,10])
ref = Scale(Sine(1/60), outscale=[0.1,10])
#trans = Scale(Sine(ref),outscale=[0,1])

trans = Sine(ref)

lmt = Mplex(trans,lmod,lca)
rmt = Mplex(trans,rca,rmod)


lenv = AM(env,lmt)
renv = AM(env,rmt)

write(lenv,renv,sps=22050,name="melvin5.wav")