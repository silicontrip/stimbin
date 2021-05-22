#!/usr/local/bin/python3

import math
from pysig import *

car = Sine(800)
wtlmod = Unitise(Square(100))

wtrmod = Unitise(Sine(20))

rmf = Linear([0,300],[0.666,3])
wtrrmod = Unitise(Sawtooth(rmf))

wtlsig = AM(car,wtlmod)
wtrsig = AM(car,wtrmod)
wtrrsig = AM(wtrsig,wtrrmod)

env = Linear([0,2,300],[DB(-96),DB(-3),DB(-3)])
wtlenv = AM(env,wtlsig)
wtrenv = AM(env,wtrrsig)

##########


culmods = Scale(Sine(rmf),outscale=[0,1])
culmodq = Scale(Square(20),outscale=[DB(-18),DB(-3)])

curmod = Scale(Square(100),outscale=[DB(-12),DB(-3)])

culsig = AM(AM(car,culmods),culmodq)
cursig = AM(car,curmod)

culenv = AM(env,culsig)
curenv = AM(env,cursig)

###

#write(wtlenv,wtrenv,sps=22050,name="wanto-cuw.wav")
#write(culenv,curenv,sps=22050,name="wanto-cuc.wav")

mplexdiv = 2
mplexfr = Div(rmf,mplexdiv)
mp = Unitise(Sine(mplexfr))

lenv = Mplex(mp,wtlenv,culenv)
renv = Mplex(mp,wtrenv,curenv)

write(lenv,renv,sps=22050,name="wanto-cu.wav")