#!/usr/local/bin/python3
import pysig as ps
import matplotlib.pyplot as pt
import numpy
import math


minhz = ps.Div(ps.DC(1.0), ps.DC(60.0))
mod = ps.Add(ps.Sine(minhz,amplitude=1.25,phase=math.pi/2.0),ps.DC(1.75)) # 0.5 - 3.0
fhz = 1.0 / 4.0
mod2 = ps.Add(ps.Sine(fhz),ps.DC(4.5)) # 3.5 - 5.5

mux = ps.Square(1.0/120.0)
modmod = ps.Mplex(mux,mod,mod2)

#fm = ps.Add(ps.Hilbert(ps.Sine(modmod,amplitude=50)),ps.DC(650))

fm = ps.DC(6000)

fcarrier = ps.Sine( ps.Add(fm,modmod) )
fcarriel = ps.Sine( ps.Add(fm,ps.Negative(modmod)) )

#am=ps.Hilbert(ps.Sine(mod,amplitude=0.2))

#am=ps.Sine(modmod,amplitude=0.2)

# easier to swap the r and l letters than the ps.Negative(am)
#carriel=ps.AM(fcarriel,ps.Add(0.4,ps.Hilbert(am)))
#carrier=ps.AM(fcarrier,ps.Add(0.4,am))

#carriel=ps.AM(fcarriel,ps.Hilbert(am))
#carrier=ps.AM(fcarrier,am)

env = ps.Linear([0,599,600],[ps.DB(-4),ps.DB(0),ps.DB(-4)])
envcar = ps.AM(env,fcarrier)
envcal = ps.AM(env,fcarriel)


ps.write(envcal,envcar,sps=22050,name="siotek2.wav")
#ps.writemono(envcar,22050,"sisq-mplex.wav")

