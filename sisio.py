#!/usr/local/bin/python3
import pysig as ps
import matplotlib.pyplot as pt
import numpy


#mod = ps.Linear([0,60,300],[0.25,8,100]) # half0-=1`
head = ps.Linear([0,30,30.1],[0.01,0.01,0.1])
tail = ps.Linear([0,48],[4,0.1])

#o = ps.Add(4,ps.AM(48,ps.Wave("348O.dfm.wav")))


ev = ps.Linear([0,0.5,299.5,300],[0,1,1,0])

spc = ps.Sine(0.1,amplitude=0.1)
spe = ps.AM(ev,spc)


ramp = ps.Linear([0,300],[0.1,2])

cs = ps.Add(ramp,spe)

hcs = ps.Cat(head,cs)
#hcso = ps.Cat(hcs,o)
smod  = ps.Cat(hcs,tail)

#smod = ps.AM(2,mod)
#mod =ps.Sine(0.01,amplitude=10)

# pt.plot(smod.getsample(numpy.arange(0,311,0.01)))
# pt.show()

fm = ps.Scale(ps.Hilbert(ps.Sine(smod)),outscale=[5950,6050])

fcarrier = ps.Sine(ps.Add(fm,smod))
fcarriel = ps.Sine(ps.Add(fm,ps.Negative(smod)))

am=ps.Sine(smod)

# easier to swap the r and l letters than the ps.Negative(am)
carriel=ps.AM(fcarriel,ps.Scale(ps.Hilbert(am),outscale=[ps.DB(-6),ps.DB(-3)]))
carrier=ps.AM(fcarrier,ps.Scale(am,outscale=[ps.DB(-6),ps.DB(-3)]))

env = ps.Linear([0,2,30,223,263,290,300],[ps.DB(-96),ps.DB(-10),ps.DB(-8),ps.DB(-6),ps.DB(-8),ps.DB(-10),ps.DB(-96)])
envcar = ps.AM(env,carrier)
envcal = ps.AM(env,carriel)


ps.write(envcal,envcar,sps=32000,name="sisio50.wav")

