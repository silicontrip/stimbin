#!/usr/local/bin/python3
import pysig as ps
import matplotlib.pyplot as pt
import numpy


#mod = ps.Linear([0,60,300],[0.25,8,100]) # half

head = ps.Linear([0,30,30.1],[0.01,0.01,0.1])
tail = ps.Linear([0,0.1,40,40.1,88],[4,16,16,4,0.1])

ev = ps.Linear([0,0.5,192.9,193.4],[0,1,1,0])

spc = ps.Sine(0.1,amplitude=0.25)
spe = ps.AM(ev,spc)


ramp = ps.Linear([0,193.4],[0.1,4])

cs = ps.Add(ramp,spe)



hcs = ps.Cat(head,cs)
mod = ps.Cat(hcs,tail)
#pt.plot(mod.getsample(numpy.arange(0,311,0.01)))
#pt.show()
smod = ps.AM(2,mod)
#mod =ps.Sine(0.01,amplitude=10)

fm = ps.Add(ps.Hilbert(ps.Sine(smod,amplitude=50)),ps.DC(100))


fcarrier = ps.Sine( ps.Add(fm,mod) )
fcarriel = ps.Sine( ps.Add(fm,ps.Negative(mod)) )

am=ps.Hilbert(ps.Sine(smod,amplitude=0.2))

# easier to swap the r and l letters than the ps.Negative(am)
carriel=ps.AM(fcarriel,ps.Add(1,ps.Hilbert(am)))
carrier=ps.AM(fcarrier,ps.Add(1,am))

env = ps.Linear([0,2,30,223,263,307,311],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-3),ps.DB(-3),ps.DB(-7),ps.DB(-96)])
envcar = ps.AM(env,carrier)
envcal = ps.AM(env,carriel)


ps.write(envcal,envcar,sps=22050,name="sisi7.wav")
#ps.writemono(envcar,22050,"sisq-mplex.wav")

