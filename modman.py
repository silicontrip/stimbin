#!/usr/local/bin/python3
import pysig as ps
import matplotlib.pyplot as pt
import numpy
import math

m3 = ps.Sine(4)
m5 = ps.Add(ps.Sine(2),1)
m5h = ps.Add( ps.Sine(2,phase=ps.DC(math.pi/2)),1)
m7 = ps.Sine(1)

fm = ps.Add(ps.AM(m3,500),ps.DC(1986))
amr = ps.Add(ps.AM(m5,ps.DB(-6)),ps.DB(-6))
aml = ps.Add(ps.AM(m5h,ps.DB(-6)),ps.DB(-6))


fcarrier = ps.Sine( ps.Add(fm,m7) )
fcarriel = ps.Sine( ps.Add(fm,ps.Negative(m7)) )

#ps.write(fcarriel,fcarrier,sps=22050,name="silvmodf5.wav")

#am=ps.AM(ps.DC(0.5),ps.Hilbert(smod))
#am=ps.AM(ps.DC(0.5),mod)

#ps.write(am,sps=22050,name="silvmod-am5.wav")


# easier to swap the r and l letters than the ps.Negative(am)
carriel=ps.AM(fcarriel,aml)
carrier=ps.AM(fcarrier,amr)

#env = ps.Linear([0,2,30,223,263,307,311],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-3),ps.DB(-3),ps.DB(-7),ps.DB(-96)])
env = ps.Linear([0,2,60,300],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-5)])

envcar = ps.AM(env,carrier)
envcal = ps.AM(env,carriel)


ps.write(envcal,envcar,sps=22050,name="modman.wav")