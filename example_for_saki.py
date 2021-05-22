#!/usr/local/bin/python3

from pysig import *


lowc = Sine(100,duration=1)
mc = Sine(900,duration=1)
hc = Sine(1000,duration=1)

mod = AM(mc,hc)
adm = Div(Add(mc,hc),2)

res = Cat(Cat(Cat(lowc,mc),hc),mod)

#write(mod,name="saki_mod.wav")
#write(lowc,name="saki_low.wav")
#write(mc,name="saki_med.wav")
#write(hc,name="saki_high.wav")

write(adm,name="saki_add.wav")
