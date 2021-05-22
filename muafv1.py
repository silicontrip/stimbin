#!/usr/local/bin/python3

<<<<<<< HEAD
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
=======
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
>>>>>>> c2ed75a8440e3f98753a7ef7f37ebb0b720606c0
