#!/usr/local/bin/python3

import math
import pysig as ps

#car = ps.Sine(665)

pha = ps.Linear([0,30],[.2,12])
cc = ps.Linear([0,30],[.2,12])
for co in range(10):
	cc = ps.Cat(cc,pha)	

fre = 665
lcar = ps.Sine(ps.Add(fre,cc))
rcar = ps.Sine(ps.Add(fre,ps.Negative(cc)))

acar = ps.AM(ps.Sine(fre),ps.Sine(cc))

#mpa = ps.Linear([0,30],[12,])
# mpx = ps.Sine(3.14159265353) #i v1 nice and irrational
#mpx = ps.Sine(6.666666) # v2
mpx = ps.Sine(0.0625) # v3

lsig = ps.Mplex(mpx,lcar,acar)
rsig = ps.Mplex(mpx,rcar,acar)

env = ps.Linear([0,2,298,300],[ps.DB(-96),ps.DB(-3),ps.DB(-3),ps.DB(-96)])

lenv = ps.AM(env,lsig)
renv = ps.AM(env,rsig)

ps.write(lenv,renv,sps=22050,name="base3.wav")
