#!/usr/local/bin/python3

import math
from pysig import *

bmf = Linear([0,360],[1,5.33333])

ms1 = AM(4,Sine(Div(bmf,4)))
ms2 = Sine(bmf)
ms3 = Div(Sine(AM(3,bmf)),3)
ms4 = Div(Sine(AM(bmf, 16)),4)

mmod = Add(ms1,Add(ms2,Add(ms3,ms4)))

fre = 440

lfre = Add(fre,mmod)
rfre = Add(fre,Negative(mmod))
lcar = Sine(lfre)
rcar = Sine(rfre)
env = Linear([0,2,358,360],[0,1,1,0])

lenv =AM(env,lcar)
renv =AM(env,rcar)

write(lenv,renv,sps=8192,name="sq-rise2.wav")