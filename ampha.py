#!/usr/local/bin/python3

import math
from pysig import *

#car = Sine(665)

#pha = Linear([0,30],[.2,12])
#cc = Linear([0,30],[.2,12])
#for co in range(10):
#	cc = Cat(cc,pha)	

cc = Scale(Sine(1/30),outscale=[0.2,12]) #v5

fre = 665
lcar = Sine(Add(fre,cc))
rcar = Sine(Add(fre,Negative(cc)))

acar = AM(Sine(fre),Sine(cc))

#mpa = Linear([0,30],[12,])
# mpx = Sine(3.14159265353) #i v1 nice and irrational
#mpx = Sine(6.666666) # v2
#mpx = Sine(0.0625) # v3
mpx = Sine(0.16666666) # v4

lsig = Mplex(mpx,lcar,acar)
rsig = Mplex(mpx,rcar,acar)

env = Linear([0,2,298,300],[DB(-96),DB(-3),DB(-3),DB(-96)])

lenv = AM(env,lsig)
renv = AM(env,rsig)

write(lenv,renv,sps=22050,name="base5.wav")
