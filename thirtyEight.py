#!/usr/local/bin/python3

import pysig as ps
import math

lcar = ps.Sine(440,phase=0)
rcar = ps.Sine(440,phase=ps.Degrees(180))

lmod = ps.Scale(ps.Sine(0.2,phase=0),outscale=[ps.DB(-8),ps.DB(-3)])
rmod = ps.Scale(ps.Sine(0.2,phase=ps.Degrees(180)),outscale=[ps.DB(-8),ps.DB(-3)])

lsig = ps.AM(lcar,lmod)
rsig = ps.AM(rcar,rmod)

env=ps.Linear([0,2,58,60],[0,1,1,0])

lenv = ps.AM(env,lsig)
renv = ps.AM(env,rsig)


ps.write(lenv,renv,sps=22050,name="thirtyEight.wav")

