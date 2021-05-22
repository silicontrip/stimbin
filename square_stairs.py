#!/usr/local/bin/python3

import math
from pysig import *

sig = DC(0,duration=0.0)

mod = Div(Sine(2000),20)

#for x in range(10):
for ss in range(10):
	nsig = Add(DC((ss-5)/10,duration=0.01),mod)
	sig = Cat(sig,nsig)
for sd in range(10):
	ss= 10 - sd
	nsig = Add(DC((ss-5)/10,duration=0.01),mod)
	sig = Cat(sig,nsig)



write(sig,sps=22050,name="stairs.wav")