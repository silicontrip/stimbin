#!/usr/local/bin/python3
import pysig as ps
import matplotlib.pyplot as pt
import numpy
import sys

mod = ps.Add ( ps.Wave(sys.argv[1]), ps.DC(1) )
#smod =ps.Hilbert(ps.Gradient(mod))

#pt.plot(smod.getsample(numpy.arange(0,251,0.01)))
#pt.show()



#smod = ps.Sine(ps.AM(2,mod))
#mod =ps.Sine(0.01,amplitude=10)
#nmod = ps.Negative(mod)


am=ps.AM(ps.DC(0.5),mod)

mfm=ps.Hilbert(mod)
fm = ps.Add(ps.AM(mfm,500),ps.DC(1986))


fcarrier = ps.Sine( ps.Add(fm,mfm) )
fcarriel = ps.Sine( ps.Add(fm,ps.Negative(mfm)) )

#ps.write(fcarriel,fcarrier,sps=22050,name="silvmodf5.wav")

#am=ps.AM(ps.DC(0.5),ps.Hilbert(smod))
#am=ps.AM(ps.DC(0.5),mod)

#ps.write(am,sps=22050,name="silvmod-am5.wav")


# easier to swap the r and l letters than the ps.Negative(am)

amh = ps.Add(ps.Hilbert(am),ps.DC(0.25))

carriel=ps.AM(fcarriel,amh)
carrier=ps.AM(fcarrier,am)

#env = ps.Linear([0,2,30,223,263,307,311],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-3),ps.DB(-3),ps.DB(-7),ps.DB(-96)])
#envcar = ps.AM(env,carrier)
#envcal = ps.AM(env,carriel)


ps.write(carriel,carrier,sps=22050,name=sys.argv[2])
