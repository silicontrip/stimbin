#!/usr/local/bin/python3
  
import math
import pysig as ps

raterate = ps.Scale(ps.Sine(1.0/7.0),outscale=[0.001,1])
frate = ps.Scale(ps.Sine(raterate),outscale=[0.001,1])
ramp=ps.Linear([0,300],[0,20]) # twenty sounds good?
#mod=ps.Div(ps.AM(ramp,ps.Sine(0.04)),20) # forty, because it's double twenty
mod=ps.Div(ps.AM(ramp,ps.Sine(frate)),20) # forty, because it's double twenty

mod90 = ps.Hilbert(mod)

#ps.write(mod,sps=11025,name="mtsi-mod.wav")

fremod = ps.Scale(mod,inscale=[-1,1],outscale=[1000,6000])

#ps.write(fremod,sps=11025,name="mtsi-fremod.wav")

lampmod = ps.Scale(mod,inscale=[-1,1],outscale=[ps.DB(-30),ps.DB(-3)])
rampmod = ps.Scale(mod90,inscale=[-1,1],outscale=[ps.DB(-30),ps.DB(-3)])

#ps.write(ampmod,sps=11025,name="mtsi-ampmod.wav")


phafre = ps.Scale(mod,outscale=[0,20])  # there's that 20 again

#ps.write(phafre,sps=11025,name="mtsi-phafre.wav")


lfre = ps.Add(fremod,phafre)
rfre = ps.Add(fremod,ps.Negative(phafre))

lpha = ps.Sine(lfre)
rpha = ps.Sine(rfre)

#ps.write(lpha,right=rpha,sps=22050,name="mtsipha.wav")

lmod = ps.AM(lampmod,lpha)
rmod = ps.AM(rampmod,rpha)

env = ps.Linear([0,2,298,300],[ps.DB(-96),ps.DB(-3),ps.DB(-3),ps.DB(-96)])

lenv=ps.AM(env,lmod)
renv=ps.AM(env,rmod)

ps.write(lenv,right=renv,sps=22050,name="mtsi-6.wav")

