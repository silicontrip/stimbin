#!/usr/local/bin/python3

#import pysig as ps
from pysig import *

pha = Div(Linear([0,600],[0.3,3]),2)
#fre = Linear([0,600],[6000,600])
fre=600
lcar = Sine(Add(fre,pha))
rcar = Sine(Add(fre,Negative(pha)))

#lmod = Sine(50)
#rmod = Sine(20)

#Scale(Sine(0.2,phase=0),outscale=[DB(-8),DB(-3)])
lmod = Scale(Sine(50),outscale=[DB(-15),DB(-5)])
rmod = Scale(Sine(20),outscale=[DB(-6),DB(-3)])

lmoca = AM(lcar,lmod)
rmoca = AM(rcar,rmod)

env = Linear([0,2,598,600],[DB(-96),DB(-3),DB(-3),DB(-96)])

lenv = AM(env,lmoca)
renv = AM(env,rmoca)

write(lenv,renv,sps=22050,name="muaf5.wav")
