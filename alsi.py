#!/usr/local/bin/python3

import pysig as ps

mod1=ps.Scale(ps.Sine(1.0/13.0),outscale=[0.1,0.5])
mod2=ps.Scale(ps.Sine(1.0/11.0),outscale=[0.1,0.5])
mod3=ps.Scale(ps.Sine(1.0/7.0),outscale=[0.1,0.5])

freq = ps.Scale(ps.Sine(mod1),outscale=[440,2000])
amp = ps.Sine(mod2)
lamp = ps.Scale(amp,outscale=[ps.DB(-6),ps.DB(0)])
#ramp = lamp
ramp = ps.Scale(ps.Hilbert(amp),outscale=[ps.DB(-10),ps.DB(-4)])

inter=ps.Div(mod3,2)
ninter = ps.Negative(inter)

lcar = ps.AM(lamp,ps.Sine(ps.Add(freq,inter)))
rcar = ps.AM(ramp,ps.Sine(ps.Add(freq,ninter)))

env=ps.Linear([0,2,298,300],[0,1,1,0])

lenv=ps.AM(env,lcar)
renv=ps.AM(env,rcar)

ps.write(lenv,right=renv,sps=22050,name='pyalsi6.wav')