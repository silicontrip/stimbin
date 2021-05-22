#!/usr/local/bin/python3
  
import math
from pysig import *

raterate = Scale(Sine(1.0/7.0),outscale=[0.001,1])
frate = Scale(Sine(raterate),outscale=[0.001,1])
ramp=Linear([0,300],[0,20]) # twenty sounds good?
#mod=Div(AM(ramp,Sine(0.04)),20) # forty, because it's double twenty
mod=Div(AM(ramp,Sine(frate)),20) # forty, because it's double twenty

mod90 = Hilbert(mod)

#write(mod,sps=11025,name="mtsi-mod.wav")

fremod = Scale(mod,inscale=[-1,1],outscale=[1000,6000])

#write(fremod,sps=11025,name="mtsi-fremod.wav")

lampmod = Scale(mod,inscale=[-1,1],outscale=[DB(-30),DB(-3)])
rampmod = Scale(mod90,inscale=[-1,1],outscale=[DB(-30),DB(-3)])

#write(ampmod,sps=11025,name="mtsi-ampmod.wav")


phafre = Scale(mod,outscale=[0,20])  # there's that 20 again

#write(phafre,sps=11025,name="mtsi-phafre.wav")


lfre = Add(fremod,phafre)
rfre = Add(fremod,Negative(phafre))

lpha = Sine(lfre)
rpha = Sine(rfre)

#write(lpha,right=rpha,sps=22050,name="mtsipha.wav")

lmod = AM(lampmod,lpha)
rmod = AM(rampmod,rpha)

env = Linear([0,2,298,300],[DB(-96),DB(-3),DB(-3),DB(-96)])

lenv=AM(env,lmod)
renv=AM(env,rmod)

write(lenv,right=renv,sps=22050,name="mtsi-6.wav")

