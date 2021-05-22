#!/usr/local/bin/python3

import math
from pysig import *
# 400Hz - 2000Hz
# -16dB - -9dB
# -13db -  -6dB

bmf = Linear([0,360],[1,5.33333])

mif = Linear([0,2,360],[DB(-16),DB(-11),DB(-11)])
maf = Linear([0,2,360],[DB(-9),DB(-3),DB(-3)])

mf = Sine(bmf)
hf = Div(mf,2.0)


fr = Scale(mf,outscale=[400,800])
# feature request, signalise the outscale values... done
am = Scale(mf,outscale=[mif,maf])

#	write(fr,sps=22050,name="eremfr.wav")
#plotsig(fr)
lfr = Sine(Add(fr, bmf))
rfr = Sine(Add(fr, Negative(bmf)))

lmod = Scale(Sine(50),outscale=[DB(-11),DB(-1)])
rmod = Scale(Sine(20),outscale=[DB(-4),DB(-1)])

#write(lfr,rfr,sps=22050,name="erenv.wav")
lenv = AM(AM(am,lfr),lmod)
renv = AM(AM(am,rfr),rmod)
write(lenv,renv,sps=22050,name="milk9.wav")