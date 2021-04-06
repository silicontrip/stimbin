#!/usr/local/bin/python3

import pysig as ps

pha = ps.Div(ps.Linear([0,600],[0.3,3]),2)
#fre = ps.Linear([0,600],[6000,600])
fre=600
lcar = ps.Sine(ps.Add(fre,pha))
rcar = ps.Sine(ps.Add(fre,ps.Negative(pha)))

#lmod = ps.Sine(50)
#rmod = ps.Sine(20)

#ps.Scale(ps.Sine(0.2,phase=0),outscale=[ps.DB(-8),ps.DB(-3)])
lmod = ps.Scale(ps.Sine(50),outscale=[ps.DB(-15),ps.DB(-5)])
rmod = ps.Scale(ps.Sine(20),outscale=[ps.DB(-6),ps.DB(-3)])

lmoca = ps.AM(lcar,lmod)
rmoca = ps.AM(rcar,rmod)

env = ps.Linear([0,2,598,600],[ps.DB(-96),ps.DB(-3),ps.DB(-3),ps.DB(-96)])

lenv = ps.AM(env,lmoca)
renv = ps.AM(env,rmoca)

ps.write(lenv,renv,sps=22050,name="muaf5.wav")
